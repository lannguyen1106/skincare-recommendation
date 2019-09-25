function submitSellForm() {
    let name = document.getElementById('name-input').value;
    let description = document.getElementById('description-input').value;
    let price = document.getElementById('price-input').value;
    let image = document.getElementById('image').value;
    if (!name || !description || !price || !parseFloat(price) || !image) {
      return alert(`Some fields might be empty or incorrect. Please make ` + 
                   `sure that all the required fields have been completed ` + 
                   `correctly, and an image has been uploaded.`);
    }
    document.getElementById('name').value = name;
    document.getElementById('description').value = description;
    document.getElementById('price').value = price;
    document.getElementById('sell-form').submit();
  };