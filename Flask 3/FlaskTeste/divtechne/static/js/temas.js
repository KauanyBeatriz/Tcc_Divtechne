if(!localStorage.tema){
    var x = (localStorage.tema) ? localStorage.tema : "claro";
    document.documentElement.setAttribute("tema", x);
  }else{
    document.documentElement.setAttribute("tema", localStorage.tema);
  }
  
  // Colocando dentro de uma variavel o id do botão do tema claro
  let toggler_tema_claro = document.getElementById("tema-toggler-claro");
  
    // Adicionando evento de click
    toggler_tema_claro.addEventListener("click", () => {
      let mudar_tema;
      let tema_atual = document.documentElement.getAttribute("tema"); // Definindo uma variavel para pegar o atributo tema atual que esta dentro da tag html
  
      // Caso o tema seja igual a claro, daltonico, escuro na tag html ele muda para o modo claro 
      if (tema_atual === "claro" || tema_atual === "daltonico" || tema_atual === "escuro") {
        mudar_tema = "claro"; // Aqui ele seta(muda) o atributo do tema na tag de html para a var mudar_tema no caso modo claro 
        localStorage.setItem('tema','claro');
      }
  
      document.documentElement.setAttribute("tema", mudar_tema);
    });
  
  
  
  let toggler_tema_escuro = document.getElementById("tema-toggler-escuro");
  
    toggler_tema_escuro.addEventListener("click", () => {
      let mudar_tema;
      let tema_atual = document.documentElement.getAttribute("tema");
     
      if (tema_atual === "claro" || tema_atual === "daltonico" || tema_atual === "escuro") {
        mudar_tema = "escuro";
        localStorage.setItem('tema','escuro');
      }
      
      document.documentElement.setAttribute("tema", mudar_tema);
    });
  
  
  
  let toggler_tema_daltonico = document.getElementById("tema-toggler-daltonico");
  
    toggler_tema_daltonico.addEventListener("click", () => {
      let mudar_tema;
      let tema_atual = document.documentElement.getAttribute("tema");
      
      if (tema_atual === "claro" || tema_atual === "daltonico" || tema_atual === "escuro") {
        mudar_tema = "daltonico";
        localStorage.setItem('tema','daltonico');
      }
      
      document.documentElement.setAttribute("tema", mudar_tema);
    });


