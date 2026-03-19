import React from "react";
import { Sparkles, BarChart3, ShieldCheck } from "lucide-react";

const EmptyAnalysisState = () => {
  return (
    <div className="h-full flex flex-col justify-center items-center text-center px-10 animate-in fade-in zoom-in duration-500">
      <div className="w-20 h-20 bg-[#D98E5E]/10 rounded-full flex items-center justify-center mb-8">
        <Sparkles size={40} className="text-[#D98E5E]" />
      </div>

      <h1 className="text-4xl font-black text-white tracking-tight mb-6 uppercase">
        AI Stock Intelligence
      </h1>

      <p className="text-[#AFA19E] text-sm max-w-md leading-7 mb-10">
        Our AI engine analyzes product stock conditions and recent sales
        behavior. Select a product from the list to generate an optimized stock
        recommendation.
      </p>

      <div className="flex gap-6">
        <div className="flex items-center gap-2 text-[10px] font-black text-[#847B78] uppercase tracking-widest">
          <BarChart3 size={14} /> Real-time Data
        </div>
        <div className="flex items-center gap-2 text-[10px] font-black text-[#847B78] uppercase tracking-widest">
          <ShieldCheck size={14} /> Secure API Layer
        </div>
      </div>
    </div>
  );
};

export default EmptyAnalysisState;