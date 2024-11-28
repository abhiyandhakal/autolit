import React, { useState } from "react";
import apiClient from "../api/apiClient";

const SearchForm = () => {
   const [keyword, setKeyword] = useState("");
   const [results, setResults] = useState(null);

   const handleSearch = async () => {
      const response = await apiClient.post("/search", { keyword });
      setResults(response.data);
   };

   return (
      <div>
         <input
            type="text"
            placeholder="Enter keyword or title"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
         />
         <button onClick={handleSearch}>Search</button>
         {results && <ResultsDisplay results={results} />}
      </div>
   );
};

export default SearchForm;
