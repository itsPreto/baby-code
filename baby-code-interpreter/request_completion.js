export async function requestCompletion(doc) {
    let responses = [];

    doc.querySelector(".hoverable").style.backgroundImage = "url('https://i.stack.imgur.com/WwxRR.gif')";
    let outputElement = doc.getElementById('#output');
    if (outputElement === null) {
      console.log("Can't find output element");
    } else {
      outputElement.textContent = "";
    }    // Add this line right after the line where you clear the 'output' value:
    doc.querySelector('.container').classList.add('fadeOutPlaceholder');
    doc.querySelector('.container').classList.remove('fadeInPlaceholder');
  
    try {
      const question = doc.getElementById('code').value;
      const codeInput = doc.getElementById('code');
      codeInput.value = '';
      codeInput.style.textAlign = "center"; 
      const messages = [
        {
          "role": "user",
          "content": question
        }
      ];
  
      appendMessage(doc, question, 'user');
  
      const response = await fetch('http://localhost:8081/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: messages
        })
      });
      
      console.log(response);
      
      if (!response.ok) {
        const message = `An error has occurred: ${response.status}`;
        throw new Error(message);
      }
      
      const data = await response.json();
  
      const code = data.choices[0].message.content;
  
      // Store the response in the responses array
      responses.push({
        message: code,
        sender: 'assistant',
      });
      appendMessage(doc, code, 'assistant');
  
      // Highlight the code
      Prism.highlightAll();
  
      doc.querySelector(".hoverable").style.backgroundImage = "url('https://i.stack.imgur.com/mJHTA.png')";
  
      doc.getElementById('output').value = code;
  
    } catch (error) {
      console.log(error);
      doc.getElementById('output').value = "Error: " + error.message;
      doc.getElementById('output').style.color = 'red';
      doc.querySelector(".hoverable").style.backgroundImage = "url('https://i.stack.imgur.com/mJHTA.png')";
    
      // Add the error message to the container
      appendMessage(doc, "Error: " + error.message, 'error');
    }
  }
  
  function appendMessage(doc, message, sender) {
    // Create new 'div', 'pre', 'code', and 'p' elements for the message
    const messageDiv = doc.createElement('div');
    const messagePre = doc.createElement('pre');
    const messageCode = doc.createElement('code');
    const messagePrefix = doc.createElement('p');
  
    // Set the 'class' and 'textContent' of the 'code' element
    if (sender === 'assistant') {
      messageCode.className = `language-python ${sender} assistant-code`;
    } else {
      messageCode.className = `language-python ${sender}`;
    }
    messageCode.textContent = message;
  
    // Set the 'textContent' of the 'p' element
    messagePrefix.textContent = sender === 'assistant' ? '<LLAMA' : sender === 'user' ? '<HUMAN' : '';
  
    messagePrefix.style.background = '#000000';  // Color for the human
    messagePrefix.style.padding = '5px';
    messagePrefix.style.borderRadius = '6px';
    // Set the background color of the 'p' element
    if (sender === 'assistant') {
      messagePrefix.style.padding = '5px';
      messagePrefix.style.borderRadius = '6px';
      messagePrefix.style.background = '#436f7e';  // Color for the llama
    } 
 
    // Set the color of error messages to red
    if (sender === 'error') {
      messageCode.style.color = 'red';
    }
  
    // Append the 'p' element to the 'pre' element
    messagePre.appendChild(messagePrefix);
  
    // Append the 'code' element to the 'pre' element
    messagePre.appendChild(messageCode);
  
    // Append the 'pre' element to the 'div' element
    messageDiv.appendChild(messagePre);
  
    // Assign the sender class to the 'div' element
    messageDiv.className = sender;
  
    // Append the 'div' element to the container div
    const container = doc.querySelector('.container');
    container.appendChild(messageDiv);

    // Scroll to the bottom of the container
    container.scrollTop = container.scrollHeight;
  
    // Apply syntax highlighting to the new code block
    Prism.highlightElement(messageCode);
}

