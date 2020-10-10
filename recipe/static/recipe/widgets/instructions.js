'use strict';
{
    const $ = django.jQuery;

    $(document).ready(function () {
        $("textarea.instructions").keyup(function () {
            var indata = { 'content': $(this).val() };
            var previewId = $(this).attr('name') + '-preview';
            $.getJSON('/api/process', indata, function (data) {
                $('#' + previewId).html(data.content);
            });
        });

        $("textarea.instructions").keyup();
    });
}