import React from "react";

const ResultsDisplay = ({ results }) => {
   return (
      <div>
         {Object.entries(results).map(([api, papers]) => (
            <div key={api}>
               <h3>{api}</h3>
               <ul>
                  {papers.map((paper, index) => (
                     <li key={index}>
                        <a href={paper.link} target="_blank" rel="noopener noreferrer">
                           {paper.title}
                        </a>{" "}
                        by {paper.authors.join(", ")}
                     </li>
                  ))}
               </ul>
            </div>
         ))}
      </div>
   );
};

export default ResultsDisplay;
