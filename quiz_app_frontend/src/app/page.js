"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Upload } from "lucide-react";

export default function QuizApp() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("http://127.0.0.1:8000/uploadfile", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          console.log("File uploaded successfully",await response.json());
        } else {
          console.error("Upload failed");
        }
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <Card className="w-full max-w-md p-6 shadow-lg rounded-2xl bg-white">
        <CardContent className="flex flex-col items-center gap-4">
          <h2 className="text-xl font-bold">Upload a Document</h2>
          <label className="cursor-pointer bg-gray-200 px-4 py-2 rounded-lg hover:bg-gray-300 transition">
            <input type="file" className="hidden" onChange={handleFileChange} />
            <div className="flex items-center gap-2">
              <Upload className="w-5 h-5" />
              <span>{file ? file.name : "Choose a file"}</span>
            </div>
          </label>
          <Button onClick={handleUpload} disabled={!file} className="w-full">
            Upload
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
