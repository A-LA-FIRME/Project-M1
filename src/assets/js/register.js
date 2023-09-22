var Register = {
    form: $("#registerForm"),

    init: function() {
        this.initForm();
    },

    initForm: function() {
        var self = this;

        this.form.validate({
            rules: {
                fullname: {
                    required: true,
                    maxlength: 128
                },
                email: {
                    required: true,
                    email: true,
                    maxlength: 128
                },
                password: {
                    required: true,
                    minlength: 8,
                    maxlength: 16
                }
            },
            messages: {
                fullname: {
                    required: "Please enter your full name",
                    maxlength: "Full name must be less than 8 characters"
                },
                email: {
                    required: "Please enter your email address",
                    email: "Please enter a valid email address"
                },
                password: {
                    required: "Please enter your password",
                    minlength: "Password must be at least 8 characters long"
                }
            },
            errorPlacement: function(error, element) {
                element.tooltip({
                    tooltipClass: "error-tooltip",
                    content: error.text(),
                    hide: {
                        effect: "fade",
                        duration: 100
                    },
                    position: {
                        my: "left top",
                        at: "right top"
                    }
                });
                element.tooltip("open");
            },
            success: function(label, element) {
                $(element).tooltip("close");
            },
            submitHandler: function(form) {
                self.send(form);
            }
        });
    },

    send: function(form) {
        var formData = $(form).serialize();
        $.post($(form).attr('action'), formData, function(response, status) {
            
            if (response.type === 'success') {
                window.location.href = response.body.message;
            } else {
                Swal.fire(
                    response.body.message,
                    '',
                    'question'
                )
            }
        });
    }     
};

$(document).ready(function() {
    Register.init();
});
