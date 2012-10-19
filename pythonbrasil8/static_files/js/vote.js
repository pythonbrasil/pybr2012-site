$(document).ready(function() {
    $('.vote-form').submit(function() {
    $.ajax({
              data: $(this).serialize(),
              type: $(this).attr('method'),
              url: $(this).attr('action'),
              success: function(response) {
                  $('#' + response.proposal_id + '-up').attr('src', imageUrl + 'up_inactive.png');
                  $('#' + response.proposal_id + '-neutral').attr('src', imageUrl + 'neutral_inactive.png');
                  $('#' + response.proposal_id + '-down').attr('src', imageUrl + 'down_inactive.png');
                  imageId = response.proposal_id + '-' + response.vote;
                  var newImageUrl = imageUrl + response.vote + '_active.png';
                  $('#' + imageId).attr('src', newImageUrl)
              }
          });
            return false;
  });
});
