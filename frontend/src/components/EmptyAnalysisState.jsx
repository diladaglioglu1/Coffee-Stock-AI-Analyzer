import React, { useState } from "react";
import { Sparkles, Search } from "lucide-react";
import { demoProducts } from "../data/demoData";

const EmptyAnalysisState = ({ onAnalyzeClick }) => {

  const [searchValue, setSearchValue] = useState("");

  const filteredProducts = demoProducts.filter((p) =>
    p.name.toLowerCase().includes(searchValue.toLowerCase())
  );

  return (
    <div className="h-full flex flex-col justify-center items-center text-center relative z-10 px-10">

      {/* AI TITLE */}
      <h1 className="flex items-center gap-4 text-4xl md:text-4xl font-black text-white tracking-tight mb-6">
        <Sparkles size={40} className="text-[#D98E5E]" />
        Inventory Intelligence
      </h1>

      {/* SUBTEXT */}
      <p className="text-[#AFA19E] text-sm md:text-base max-w-xl leading-7 mb-10">
        Get clear stock insights for your coffee products. 
        Select a product from the list or type a product name below to start AI analysis.
      </p>


      {/* SEARCH INPUT */}
      <div className="w-full max-w-md mb-6 relative">

        <Search
          size={18}
          className="absolute left-4 top-4 text-[#847B78]"
        />

        <input
          type="text"
          placeholder="Type product name..."
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          className="w-full bg-[#2A1D1A] border border-white/10 rounded-2xl py-4 pl-10 pr-4 text-white text-sm focus:ring-1 focus:ring-[#D98E5E] outline-none"
        />

      </div>


      {/* SEARCH RESULTS */}
      {searchValue && (
        <div className="w-full max-w-md mb-6 bg-[#2A1D1A] rounded-2xl border border-white/10 overflow-hidden">

          {filteredProducts.length === 0 && (
            <p className="text-sm text-[#AFA19E] p-4">
              No matching product found
            </p>
          )}

          {filteredProducts.map((product) => (
            <div
              key={product.id}
              onClick={() => {
                onAnalyzeClick(product.id);
              }}
              className="px-4 py-3 text-left text-sm text-white hover:bg-[#3a2722] cursor-pointer transition"
            >
              {product.name}
            </div>
          ))}
        </div>
      )}


      {/* ANALYZE BUTTON */}
      <button
        onClick={onAnalyzeClick}
        className="px-10 py-4 bg-[#D98E5E] hover:bg-[#C47D4D] text-white rounded-2xl font-black uppercase tracking-[0.3em] text-[10px] transition-all shadow-lg shadow-orange-950/30 flex items-center gap-2"
      >
        <Sparkles size={16} />
        AI STOCK ANALYSIS
      </button>

    </div>
  );
};

export default EmptyAnalysisState;