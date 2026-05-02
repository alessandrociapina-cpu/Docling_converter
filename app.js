document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('pdf-file');
    const resultDiv = document.getElementById('result');
    const statusText = document.getElementById('status');
    
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    // Aviso de processamento pesado
    statusText.innerText = 'Enviando PDF para o servidor. O Docling está reconstruindo a estrutura...';
    resultDiv.innerHTML = '';
    
    try {
        // ATENÇÃO: Substitua a URL abaixo pela URL gerada pelo Render/Railway
        const response = await fetch('https://SUA-API-NO-RENDER.onrender.com/process-pdf/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Erro no servidor: ${response.statusText}`);
        }

        const data = await response.json();
        
        statusText.innerText = 'Processamento concluído. Texto pronto para análise da IA.';
        resultDiv.innerHTML = `<pre>${data.markdown}</pre>`;
        
    } catch (error) {
        console.error(error);
        statusText.innerText = 'Falha na comunicação. Verifique se a API está online e se o arquivo não excedeu o limite de memória.';
    }
});
