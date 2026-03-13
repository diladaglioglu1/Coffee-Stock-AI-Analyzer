import React from "react";

const SummaryCard = ({
  icon,
  title,
  value,
  subtitle,
  accent = "text-[#D98E5E]",
}) => {
  return (
    <div className="bg-white border border-[#E9DED4] rounded-[2rem] p-6 shadow-sm">
      <div className={`flex items-center gap-3 mb-3 ${accent}`}>
        {icon}
        <span className="text-[11px] font-black uppercase tracking-[0.2em]">
          {title}
        </span>
      </div>
      <p className="text-3xl font-black text-[#1F1311]">{value}</p>
      <p className="text-sm text-[#847B78] mt-1">{subtitle}</p>
    </div>
  );
};

export default SummaryCard;