$(document).ready(function() {
    $('#speech-form').on('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/speech-to-text',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.success) {
                    $('#speech-result').text("Transcription: " + data.transcription);
                } else {
                    $('#speech-result').text("Error: " + data.error);
                }
            }
        });
    });

    $('#behavior-form').on('submit', function(event) {
        event.preventDefault();
        var formData = {
            'age': $('#age').val(),
            'sentence_length': $('#sentence_length').val(),
            'education_level': $('#education_level').val(),
            'behavior_score': $('#behavior_score').val()
        };
        $.ajax({
            url: '/behavior-analysis',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(data) {
                $('#behavior-result').text("Recommendation: " + data.recommendation);
            }
        });
    });
});
