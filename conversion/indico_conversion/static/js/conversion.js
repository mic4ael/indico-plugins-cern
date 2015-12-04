(function() {
    'use strict';

    function checkConversion(ids) {
        $.ajax({
            url: ConversionPlugin.urls.check,
            method: 'GET',
            data: {a: ids},
            error: handleAjaxError,
            success: function(data) {
                if (handleAjaxError(data)) {
                    return;
                }

                if (data.pending.length) {
                    setTimeout(function() {
                        checkConversion(data.pending);
                    }, 10000);
                }

                _.each(data.finished, function(id) {
                    var placeholder = $('.pdf-pending[data-attachment-id="{0}"]'.format(id));
                    if (id in data.containers) {
                        var newContainer = $(data.containers[id]);
                        placeholder.closest('.attachments-display-container').replaceWith(newContainer);
                        newContainer.find('.attachments > .dropdown').parent().dropdown();
                    }
                });
            }
        });
    }

    $(document).ready(function() {
        var ids = $('.pdf-pending').map(function() {
            return $(this).data('attachmentId');
        }).get();
        if (ids.length) {
            setTimeout(function() {
                checkConversion(ids);
            }, 5000);
        }
    });
})();
