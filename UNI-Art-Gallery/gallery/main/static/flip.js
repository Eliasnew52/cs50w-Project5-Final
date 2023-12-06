document.addEventListener('DOMContentLoaded', function() {
  // Get references to your buttons
  var form = document.querySelector('.form');
  var flipButton = document.querySelector('.btn-flip');


  // Add event listener for the "Siguiente" button
  flipButton.addEventListener('click', function() {
      // Toggle the 'clicked' class
      form.classList.toggle('clicked');
      
  });

  
});