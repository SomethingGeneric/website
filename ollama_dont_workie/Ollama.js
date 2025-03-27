import React from 'react';

async function fetchGeneratedHtml() {
  const response = await fetch('https://ol.mattcompton.dev/api/generate', {
    method: 'POST',
    mode: 'no-cors',
    headers: {
      'Content-Type': 'application/json',
      'Origin': 'http://localhost',
    },
    body: JSON.stringify({
      model: 'llama3.2',
      prompt: "please generate html of a page for a company named Mattcompton.dev LLC 501c nonprofit. it can be simple as it will be parsed by other programs, but please ensure it is complete and loadable by a web browser. DO NOT RETURN ANYTHING BUT THE HTML",
      stream: false,
    }),
  });

  const data = await response.json();
  const result = decodeURIComponent(data['response']);
  console.log('Result:', result);
  return result;
}

export default function Ollama() {
  const [htmlContent, setHtmlContent] = React.useState('');
  const [isValidHtml, setIsValidHtml] = React.useState(false);

  React.useEffect(() => {
    async function fetchData() {
      try {
        const html = await fetchGeneratedHtml();
        console.log('Fetched HTML:', html);
        // Check if the HTML is valid by attempting to parse it
        const parser = new DOMParser();
        const parsedDoc = parser.parseFromString(html, 'text/html');
        const isHtmlValid = !parsedDoc.querySelector('parsererror');

        setIsValidHtml(isHtmlValid);
        setHtmlContent(html);
      } catch (error) {
        console.error('Error fetching HTML:', error);
        setIsValidHtml(false);
        setHtmlContent("<p>Sorry, there was an error fetching the content.</p><br/><pre><code>" + error + "</code></pre>");
      }
    }

    fetchData();
  }, []);

  return isValidHtml ? (
    <div dangerouslySetInnerHTML={{ __html: htmlContent }}></div>
  ) : (
    <pre><code>{htmlContent}</code></pre>
  );
}