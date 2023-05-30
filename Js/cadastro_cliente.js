
        var current_fs, next_fs, previous_fs; //fieldsets
        var opacity;
        var current = 1;
        var steps = $("fieldset").length;
        
        setProgressBar(current);
        
        $(".next").click(function(){
        
            current_fs = $(this).parent();
            next_fs = $(this).parent().next();
            
            //Add Class Active
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
            
            //show the next fieldset
            next_fs.show();
            //hide the current fieldset with style
            current_fs.animate({opacity: 0}, {
                step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;
                
                current_fs.css({
                'display': 'none',
                'position': 'relative'
                });
                next_fs.css({'opacity': opacity});
                },
                duration: 500
            });
            setProgressBar(++current);
        });
        
        $(".previous").click(function(){
        
            current_fs = $(this).parent();
            previous_fs = $(this).parent().prev();
            
            //Remove class active
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
            
            //show the previous fieldset
            previous_fs.show();
            
            //hide the current fieldset with style
            current_fs.animate({opacity: 0}, {
                step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;
                
                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                previous_fs.css({'opacity': opacity});
                },
                duration: 500
            });
            setProgressBar(--current);
        });
        
        function setProgressBar(curStep){
            var percent = parseFloat(100 / steps) * curStep;
            percent = percent.toFixed();
            $(".progress-bar").css("width",percent+"%");
        }
        $(".submit").click(function(){
            
        });



        

       
        const cad_cliente = document.getElementById('cad_cliente');

        let nome = document.querySelector('#nm_cliente');
        let email = document.querySelector('#email_cliente');
        let senha = document.querySelector('#senha_cliente');
        let cnpj = document.querySelector('#cnpj');
        //let tipo = document.querySelector('#tipo');
        let dt_nasc = document.querySelector('#dt_nasc_cliente');
        let telefone = document.querySelector('#telefone_cliente');
        let nacionalidade = document.querySelector('#nacionalidade');
        let facebook = document.querySelector('#facebook_cliente');
        let instagram = document.querySelector('#instagram_cliente');
        let outros = document.querySelector('#outros');

            
            
            cad_cliente.addEventListener('click',function(){
            
            let form = new FormData();
            form.append('nome',nome.value);
            form.append('email',email.value);
            form.append('senha',senha.value);
            form.append('cnpj',cnpj.value);
           // form.append('tipo',tipo.value);            
            form.append('dt_nasc',dt_nasc.value);
            form.append('telefone',telefone.value);
            form.append('nacionalidade',nacionalidade.value);
            form.append('facebook',facebook.value);
            form.append('instagram',instagram.value);
            form.append('outros',outros.value);
            
                fetch(url,{
                    body:form,
                    method:'POST'
                })
                .then(function(data){
                    return data.text();
                })
                .then(function(data){
                    alert(data);
                });
        
            
        });
