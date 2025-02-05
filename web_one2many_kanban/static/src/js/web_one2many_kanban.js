odoo.define('web_one2many_kanban.web_one2many_kanban', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var KanbanRecord = require('web.KanbanRecord');

    KanbanRecord.include( {
        _render: function () {
            var self = this;
            var self_super = self._super;
            var self_super_args = arguments;
            var o2x_field_names = [];
            _.each(this.fieldsInfo, function (field_info, field_nm) {
                if (field_info.mode === 'list' || field_info.mode === 'kanban')
                {
                    o2x_field_names.push(field_nm);
                }
            });

            if ( o2x_field_names.length > 0) {
                var o2x_records = [];
                var o2x_recordData = [];
                _.each(o2x_field_names, function (o2x_field_name) {
                    var record = self.qweb_context.record[o2x_field_name];
                    if (record.type === 'one2many') {
                        o2x_records.push(record);
                        o2x_recordData.push(self.recordData[o2x_field_name])
                    }
                });
                var def = ajax.jsonRpc(
                    "/web/fetch_x2m_data",
                    "call",
                    {'o2x_records': o2x_records, 'o2x_record_data': o2x_recordData}).then(function (o2x_datas) {
                    for (var i=0; i<o2x_datas.length; i++) {
                        o2x_records[i].raw_value = o2x_datas[i];
                    }
                });
                return def.then(function () {
                    self_super.apply(self, self_super_args);
                });
            } else {
                return self._super.apply(self, arguments);
            }

        },
    });
});
