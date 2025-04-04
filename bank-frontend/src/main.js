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
helloText.style.fontSize = "30px";
helloText.style.fontWeight = "bold"; 
helloText.style.fontFamily = "Comic Sans MS, cursive"; // You know I had to do it to em
helloText.style.textAlign = "center";
helloText.style.textShadow = "2px 2px 4px black"; // Adds a black outline effect to text, works with ou scheme

// Append text object to body
document.body.appendChild(helloText);

//for the meme
const subText = document.createElement("p");
subText.innerHTML = "Loan Department Update: Nicholas has <u>denied</u> your request before you even applied.";
subText.style.color = "red";
subText.style.fontSize = "24px";
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

// Create a menu button
const menuButton = document.createElement("button");
menuButton.innerHTML = "&#9776;"; 
menuButton.style.position = "fixed";
menuButton.style.top = "10px";
menuButton.style.left = "10px";
menuButton.style.background = "gold";
menuButton.style.color = "black";
menuButton.style.border = "none";
menuButton.style.padding = "10px";
menuButton.style.fontSize = "24px";
menuButton.style.cursor = "pointer";
menuButton.style.zIndex = "1000";
document.body.appendChild(menuButton);

// Create a sidebar container
const sidebar = document.createElement("div");
sidebar.style.position = "fixed";
sidebar.style.left = "-220px"; // Initially hidden
sidebar.style.top = "0";
sidebar.style.width = "200px";
sidebar.style.height = "100vh";
sidebar.style.background = "#333";
sidebar.style.padding = "80px 10px 10px"; // Add top padding to avoid overlap
sidebar.style.display = "flex";
sidebar.style.flexDirection = "column";
sidebar.style.alignItems = "center";
sidebar.style.boxShadow = "2px 0 5px rgba(0,0,0,0.5)";
sidebar.style.transition = "left 0.3s ease";
document.body.appendChild(sidebar);

// Toggle sidebar visibility
menuButton.addEventListener("click", () => {
    if (sidebar.style.left === "0px") {
        sidebar.style.left = "-220px";
    } else {
        sidebar.style.left = "0px";
    }
});

const tableNames = [
    {name :"Accounts", url : "accounts.html"},
    {name :"Banks", url : "banks.html"},
    {name :"Loans", url : "loans.html"},
    {name :"People", url : "people.html"},
    {name :"Transactions", url : "transactions.html"}];

// Function to create sidebar buttons
function createSidebarButton(name, url) {
    const button = document.createElement("button");
    button.textContent = name;
    button.style.width = "100%";
    button.style.margin = "10px 0"; // Increase margin for better spacing
    button.style.padding = "10px";
    button.style.background = "gold";
    button.style.color = "black";
    button.style.border = "none";
    button.style.cursor = "pointer";
    button.style.fontWeight = "bold";
    
    //Adding code to have buttons go to their respective html pages.
    button.addEventListener("click", () => {
        window.location.href = url;
    });


    sidebar.appendChild(button);
}

// Generate buttons for each table -updated args for urls
tableNames.forEach(table => createSidebarButton(table.name, table.url));

// Create footer container
const footer = document.createElement("footer");
footer.style.position = "fixed";
footer.style.bottom = "0";
footer.style.width = "100%";
footer.style.background = "#222";
footer.style.color = "white";
footer.style.textAlign = "center";
footer.style.padding = "10px 0";

// Create a logo image element
const logoImage = document.createElement("img");
logoImage.src = "logo.png";
logoImage.alt = "Bank Logo";
logoImage.style.display = "block";
logoImage.style.margin = "20px auto";
logoImage.style.maxWidth = "300px";
logoImage.loading = "eager";
document.body.appendChild(logoImage);

// Footer links
const footerLinks = [
    { text: "Feedback", url: "#" },
    { text: "Contact Us", url: "#" },
    { text: "About Us", url: "#" },
    { text: "Privacy Policy", url: "#" }
];

footerLinks.forEach(linkData => {
    const link = document.createElement("a");
    link.textContent = linkData.text;
    link.href = linkData.url;
    link.style.color = "gold";
    link.style.margin = "0 15px";
    link.style.textDecoration = "none";
    link.style.fontWeight = "bold";
    
    link.addEventListener("mouseover", () => link.style.textDecoration = "underline");
    link.addEventListener("mouseout", () => link.style.textDecoration = "none");
    
    footer.appendChild(link);
});

document.body.appendChild(footer);


setTimeout(() => {
    reviewingText.innerHTML = "❌ <b>Loan Denied.</b> Nicholas didn't even open the request.";
    reviewingText.style.color = "red";
}, 3000); // Wait 3 seconds before crushing hopes

