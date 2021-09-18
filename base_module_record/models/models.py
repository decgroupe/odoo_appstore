import string
import uuid
import io
import psycopg2, psycopg2.extensions

from odoo import models


class BaseModel(models.BaseModel):
    _inherit = 'base'

    def _get_xml_record_human_name(self):
        self.ensure_one()
        try:
            rec_name = self[self._rec_name] or ''
            name = list(
                filter(lambda x: x in string.ascii_letters, rec_name.lower())
            )
            name = ''.join(name)
        except:
            name = ''
        if name:
            name = "%d__%s" % (self.id, name)
        else:
            name = uuid.uuid4().hex[:8]
        return "%s_%s" % (self._table, name)

    def ensure_human_xml_id(self, skip=False):
        """ Create missing external ids for records in ``self``, and return an
            iterator of pairs ``(record, xmlid)`` for the records in ``self``.

        :rtype: Iterable[Model, str | None]
        """
        if skip:
            return ((record, None) for record in self)

        if not self:
            return iter([])

        if not self._is_an_ordinary_table():
            raise Exception(
                "You can not export the column ID of model %s, because the "
                "table %s is not an ordinary table." %
                (self._name, self._table)
            )

        modname = '__module__'

        cr = self.env.cr
        cr.execute(
            """
            SELECT res_id, module, name
            FROM ir_model_data
            WHERE model = %s AND res_id in %s
        """, (self._name, tuple(self.ids))
        )
        xids = {
            res_id: (module, name)
            for res_id, module, name in cr.fetchall()
        }

        def to_xid(record_id):
            (module, name) = xids[record_id]
            return ('%s.%s' % (module, name)) if module else name

        # create missing xml ids
        missing = self.filtered(lambda r: r.id not in xids)
        if missing:
            xids.update(
                (r.id, (modname, r._get_xml_record_human_name()))
                for r in missing
            )
            fields = ['module', 'model', 'name', 'res_id']

            # disable eventual async callback / support for the extent of
            # the COPY FROM, as these are apparently incompatible
            callback = psycopg2.extensions.get_wait_callback()
            psycopg2.extensions.set_wait_callback(None)
            try:
                cr.copy_from(
                    io.StringIO(
                        u'\n'.join(
                            u"%s\t%s\t%s\t%d" % (
                                modname,
                                record._name,
                                xids[record.id][1],
                                record.id,
                            ) for record in missing
                        )
                    ),
                    table='ir_model_data',
                    columns=fields,
                )
            finally:
                psycopg2.extensions.set_wait_callback(callback)
            self.env['ir.model.data'].invalidate_cache(fnames=fields)

        return ((record, to_xid(record.id)) for record in self)
