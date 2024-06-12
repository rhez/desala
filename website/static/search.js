
async function search(lines, query) {
  let matching_lines = {desala:[], gen:[]};
  let context_len = 2;
  let words = await associate(lines, context_len);
  let gen = await getContext(words, context_len).split("\n");
  matching_lines["desala"] = lines.filter(line => line.includes(query));
  matching_lines["gen"] = gen.filter(line => line.includes(query));
  return matching_lines;
}

window.onload = async function(){

  const lines = await fetch('/lines').then(response => response.text()).then(json => JSON.parse(json));

  // Get the quote of the day
  const quote = await fetch('/qotd').then(response => response.text());
  const qotd = document.getElementById("qotd");
  qotd.textContent = quote;

  const searchForm = document.getElementById("search-form");
  const searchInput = document.getElementById("search-input");
  const searchResults = document.getElementById("search-results");

  let response = "";

  searchForm.addEventListener("submit", (event) => {
    // Prevent the form from submitting and refreshing the page
    event.preventDefault();

    const captchaForm = document.getElementById("captcha");

    if(captchaForm){
      response = grecaptcha.getResponse(); // get the reCAPTCHA response
    }

    if (response.length > 0) { // check if the response is valid
      // Remove the captcha div
      if(captchaForm){
        captchaForm.remove();
      }
      
      // Get container element
      const container2 = document.getElementById('container2');

      container2.style.justifyContent = "flex-start";
      
      // Get the search query from the input field
      const query = searchInput.value.toLowerCase();

      // Clear the search results list
      searchResults.innerHTML = "";

      // Search the database and add the results to the list
      search(lines, query).then(data => {
        const combined = data["desala"].concat(data["gen"]);
        // Shuffle the combined array
        for (let i = combined.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [combined[i], combined[j]] = [combined[j], combined[i]];
        }
        // Iterate over the combined array
        for (const item of combined) {
            const div = document.createElement("div");
            div.textContent = item;
            // Check if the item is from the "gen" array
            if (data["gen"].includes(item)) div.style.color = "#0f0";
            searchResults.appendChild(div);
        }
      });

    } else {
      alert("Please complete the reCAPTCHA challenge before submitting the form.");
    }

  });

}
