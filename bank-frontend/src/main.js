console.log("From main.js")

//BACKGROUND COLOR *TESTING*-------------------------------------------

//document.body.style.backgroundColor = "#FAF3DD"; // Light beige

//document.body.style.backgroundColor = "#EAD196"; // Soft gold, not too harsh

//document.body.style.background = "linear-gradient(to right, #FAF3DD, #EAD196)";// Beige to gold gradient

// This uses OU colors but might be too much?? have fun messing around with the other ones
document.body.style.background = "linear-gradient(to right, #000000, #C5A30F)";

//--------------------------------------------------------------------


// Creating text to check if page loads correctly
// Creating a text object
const helloText = document.createElement("p");
helloText.textContent = "💰 Welcome to our Bank App! Your money is (probably) safe. 💸"; 
helloText.style.color = "gold"; 
helloText.style.fontSize = "24px";
helloText.style.fontWeight = "bold"; 
helloText.style.fontFamily = "Comic Sans MS, cursive"; // You know I had to do it to em
helloText.style.textAlign = "center";
helloText.style.textShadow = "2px 2px 4px black"; // Adds a black outline effect to text, works with ou scheme

// Append text object to body
document.body.appendChild(helloText);

//for the meme
const subText = document.createElement("p");
subText.innerHTML = "Loan Department Update: Gavin has <u>denied</u> your request before you even applied.";
subText.style.color = "red";
subText.style.fontSize = "18px";
subText.style.fontStyle = "italic";
subText.style.textAlign = "center";
subText.style.textShadow = "2px 2px 4px black";

// Append subtext
document.body.appendChild(subText);

//for the meme
const reviewingText = document.createElement("p");
reviewingText.textContent = "🔄 Gavin is reviewing your loan request...";
reviewingText.style.color = "yellow";
reviewingText.style.fontSize = "18px";
reviewingText.style.fontStyle = "italic";
document.body.appendChild(reviewingText);
reviewingText.style.textAlign = "center";
reviewingText.style.textShadow = "2px 2px 4px black"; 

setTimeout(() => {
    reviewingText.innerHTML = "❌ <b>Loan Denied.</b> Gavin didn't even open the request.";
    reviewingText.style.color = "red";
}, 3000); // Wait 3 seconds before crushing hopes

