(function($, global){
    $(document).ready(function(){
        $("#add-speaker > a").click(function(e) {
            e.stopPropagation();
            e.preventDefault();
            $(this).parent().before('<span><input type="text" name="extra_speakers" value="'+nameOrEmail+'" /><a href="#" title="Remove speaker" class="remove-speaker">Remove</a></span>');
        });

        $("#send-proposal form > p > span").delegate("input", "focus", function() {
            var value = $(this).val();
            if (value === nameOrEmail) {
                $(this).val("");
            }
        }).delegate("input", "blur", function() {
            var value = $(this).val();
            if (value === "") {
                $(this).val(nameOrEmail);
            }
        }).delegate("a.remove-speaker", "click", function(e) {
            e.stopPropagation();
            e.preventDefault();
            $(this).parent().remove();
        });
    });

    global.confirmDelete = function(msg, url, id) {
        if (confirm(msg)) {
            global.location.href = url;
        }
    };
})(window.jQuery, window);
