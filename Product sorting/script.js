document.getElementById("priceForm").addEventListener("submit", async function (event) {
    event.preventDefault();
  
    const formData = new FormData(event.target);
    const data = {
      minPrice: formData.get("minPrice"),
      maxPrice: formData.get("maxPrice"),
      email: formData.get("email"),
    };
  
    try {
      const response = await fetch("/filter", {
        method: "POST",
        body: new URLSearchParams(data),
      });
      const result = await response.json();
      alert(result.message || result.error);
    } catch (error) {
      console.error(error);
      alert("An error occurred. Please try again.");
    }
  });
  