/*
import React, { useState } from "react";
import axios from "axios";


const ImageUpload = ({ onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Upload successful:", response.data);

      

      //response.data has everything
      if (onUploadSuccess) {
        onUploadSuccess(response.data); // Pass data back to parent
      }


    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default ImageUpload;
*/


import React, { useState } from "react";
import axios from "axios";

const ImageUpload = ({ onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null); // For displaying image preview

  const handleFileChange = (event) => {
    if (event.target.files) {
      const file = event.target.files[0];
      setSelectedFile(file);

      // If it's an image, create a preview URL
      if (file && file.type.startsWith("image/")) {
        const url = URL.createObjectURL(file);
        setPreviewUrl(url);
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Upload successful:", response.data);

      //response.data has everything
      if (onUploadSuccess) {
        onUploadSuccess(response.data); // Pass data back to parent
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>

      {previewUrl && (
        <div>
          <h4>File Preview:</h4>
          <img src={previewUrl} alt="File Preview" style={{ maxWidth: "300px" }} />
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
