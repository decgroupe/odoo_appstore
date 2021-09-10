/* Copyright 2016, 2019 Openworx.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

// Check if debug mode is active and then add debug into URL when clicking on the App sidebar
odoo.define('backend_theme_v12.Sidebar', function (require) {
    "use strict";
    var core = require('web.core');
    var session = require('web.session');
    var Widget = require('web.Widget');
    $(function () {
        (function ($) {
            $.addDebug = function (url) {
                url = url.replace(/(.{4})/, "$1?debug");
                return url;
            }
            $.addDebugWithAssets = function (url) {
                url = url.replace(/(.{4})/, "$1?debug=assets");
                return url;
            }
            $.delDebug = function (url) {
                var str = url.match(/web(\S*)#/);
                url = url.replace("str/g", "");
                return url;
            }
        })(jQuery);
        $("#sidebar a").each(function () {
            var url = $(this).attr('href');
            if (session.debug == 1) $(this).attr('href', $.addDebug(url));
            if (session.debug == 'assets') $(this).attr('href', $.addDebugWithAssets(url));
            if (session.debug == false) $(this).attr('href', $.delDebug(url));
        });
        $("#sidebar a").click(function () {
            var img = $(this).children('.app-sidebar-menuitem');
            img.removeClass('app-sidebar-menuitem-wait');
            img.addClass('app-sidebar-menuitem-active');
            setTimeout(function () {
                img.removeClass('app-sidebar-menuitem-active');
                img.addClass('app-sidebar-menuitem-wait');
            }, 3000);
            var favicon_link = $("[rel='shortcut icon']");
            favicon_link.attr("href" , img.attr("src"));
        });
    });
});
