$("#form").submit(function (event) {
  event.preventDefault();

  var $form = $(this);
  var ajaxloader = $form.find('#ajaxloader');
  var button = $form.find('[type=submit]');

  button.hide();
  ajaxloader.show();

  var posting = $.post("/", $form.serialize());
  posting.done(function(data) {
    ajaxloader.hide();
    button.show();
    alert(data);
  })
});
