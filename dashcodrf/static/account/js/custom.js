"use strict";
var App = {
    handleCustomFileInput: function () {
        $(".custom-file > .custom-file-label").each(function () {
            var e = $(this).text();
            $(this).data("label", e)
        }), $(document).on("change", ".custom-file > .custom-file-input", function () {
            var e = this.files, o = $(this).next(".custom-file-label"), n = o.data("label");
            if (o.text(e.length + " files selected"), e.length <= 2) {
                for (var t = [], a = 0; a < e.length; a++) t.push(e[a].name);
                o.text(t.join(", "))
            }
            e.length || o.text(n)
        })
    }, handlePasswordVisibility: function () {
        $(document).on("click", '[data-toggle="password"]', function (e) {
            e.preventDefault();
            var o = $(this).attr("href"), n = $(o);
            $(this).has(".fa") && $(this).children(".fa, .far").toggleClass("fa-eye fa-eye-slash"), n.is('[type="password"]') ? (n.prop("type", "text"), $(this).children().last().text("Hide")) : (n.prop("type", "password"), $(this).children().last().text("Show"))
        })
    }
}, Dash = App.handleCustomFileInput();

$("#id_phone").mask('(000) 000-0000');