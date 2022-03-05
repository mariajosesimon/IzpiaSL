const btnDelete = document.querySelectorAll('.btn-delete')
if(btnDelete){
   const btnArrayDelete= Array.from(btnDelete);
   btnArrayDelete.forEach((btn)=>{
       console.log("en eliminar")
    btn.addEventListener('click', (e)=>{
        if(!confirm("Quieres eliminar la imagen? ")){
            e.preventDefault();
            console.log('Elimnada')
        }
    })

   });
}

/*
Mostrar imagenes. 
https://css-tricks.com/how-to-show-images-on-click/ */

document.querySelectorAll(".display_image").forEach((item) => {
    item.addEventListener("click", (event) => {
      const href = event.target.getAttribute("href");
      const newImage = document.createElement("img");
      event.preventDefault();
      newImage.setAttribute("src", href);
      document.body.insertBefore(newImage, event.target);
      event.target.remove();
    });
  });