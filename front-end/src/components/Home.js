import React from 'react';
import './style.css';
import './Home.css';

const Home = () => {
  return (
    <>
    <nav className="navbar">
    <div className="container-fluid">
      <a className="navbar-brand" href="#">NutriPass</a>
    </div>
    </nav>
    <div className='welcome'>
      <h1>Welcome to NutriPass</h1>
      <h3>Your go-to solution for dietary needs!</h3>
      <a href="/shop">Go to Shop</a>
    </div>
    <div class="accordion" id="accordionExample">
  <div class="accordion-item">
    <h2 class="accordion-header">
      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
      Target Audience
      </button>
    </h2>
    <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
      <div class="accordion-body">
        <strong>Who It’s For:</strong> This project is designed for users with specific dietary needs or restrictions who want a quick, reliable way to filter out foods that contain undesired ingredients, especially when grocery shopping online.
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
      Purpose
      </button>
    </h2>
    <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
      <div class="accordion-body">
        <strong>Why It’s Needed:</strong> Many people have food sensitivities, allergies, or dietary preferences, making label-checking essential. This tool simplifies the process by providing only the relevant product options, saving users time and reducing the chance of accidentally purchasing unsuitable items.
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
      Value and Impact
      </button>
    </h2>
    <div id="collapseThree" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
      <div class="accordion-body">
        <strong>User Experience:</strong> By automating the ingredient-filtering process, the project provides a more accessible and streamlined shopping experience for users with dietary restrictions.
      </div>
    </div>
  </div>
</div>

    <footer>Aby Huerta 2024</footer>
    </>
  );
};

export default Home;
