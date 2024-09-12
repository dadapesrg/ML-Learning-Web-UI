const express = require('express');
const { Storage } = require('@google-cloud/storage');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.json());

const storage = new Storage({
    keyFilename: 'path-to-your-service-account.json',  // Replace with your service account credentials
    projectId: 'your-project-id'  // Replace with your project ID
});

const bucketName = 'your-bucket-name';  // Replace with your Google Cloud Storage bucket name

app.post('/upload-json', async (req, res) => {
    try {
        const data = JSON.stringify(req.body);
        const filename = `json-${Date.now()}.json`;
        const file = storage.bucket(bucketName).file(filename);
        await file.save(data);
        
        res.json({ message: `File ${filename} uploaded to ${bucketName}.` });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});
