(function () {

    $("form").submit(function () {
        const val = $(this).val().toLowerCase();
        const regex = new RegExp("(.*?)\.(csv)$");
        if (!(regex.test(val))) {
            $(this).val('');
            alert('Only csv file can be uploaded');
            return false;
        }

    });

}());
