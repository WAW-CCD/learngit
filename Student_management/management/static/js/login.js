$(document).ready(function(){

  $('.dropdown').dropdown();
  $('.ui.checkbox').checkbox();

  $('.formexample .form')
  .form({
    on: 'blur',
    fields: {
      username: {
        identifier  : 'username',
        rules: [
          {
            type   : 'empty',
            prompt : '用户名不能为空'
          },
            {
                type:'number',
                prompt:'用户名只能是数字'
            }
        ]
      },

      password: {
        identifier  : 'password',
        rules: [
            {
              type: 'empty',
              prompt: '密码不能为空'
            }
      ]
      }


    }
  });

})


$('.menu .item')
  .tab()
;

