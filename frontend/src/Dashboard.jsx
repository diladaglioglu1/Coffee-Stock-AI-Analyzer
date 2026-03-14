import React, { useMemo, useState } from "react";
import { TriangleAlert, Sparkles, Package, TrendingUp, Search } from "lucide-react";

import MainLayout from "./layout/MainLayout";
import ProductCard from "./components/ProductCard";
import ProductListItem from "./components/ProductListItem";
import SummaryCard from "./components/SummaryCard";
import EmptyAnalysisState from "./components/EmptyAnalysisState";
import AnalysisModal from "./components/AnalysisModal";

import { demoProducts } from "./data/demoData";

const Dashboard = () => {
  // Ekranda gezinme ve veri yönetimi için gerekli tüm state'ler
  const [activeTab, setActiveTab] = useState("dashboard");
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [selectedProductId, setSelectedProductId] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [productSearch, setProductSearch] = useState("");

  // Ürün seçimlerini ve filtrelemeleri hesapla
  const featuredProducts = useMemo(() => demoProducts.slice(0, 4), []);
  const selectedProduct =
    demoProducts.find((item) => item.id === selectedProductId) || null;

  const filteredProducts = demoProducts.filter((item) =>
    item.name.toLowerCase().includes(productSearch.toLowerCase())
  );

  // BACKEND BAĞLANTI FONKSİYONU
  const handleAnalyze = async () => {
    if (!selectedProduct) return;

    setIsAnalyzing(true);

    try {
      // Python Backend (FastAPI) isteği
      const response = await fetch(`http://localhost:8000/api/ai/analyze/${selectedProduct.id}`);

      if (!response.ok) {
        throw new Error("Backend'den cevap alınamadı.");
      }

      const data = await response.json();

      // Backend'den gelen veriyi Modal'ın beklediği formata dönüştür
      const formattedData = {
        product_name: data.product_name,
        current_stock: data.current_stock || selectedProduct.current_stock,
        average_daily_sales: data.average_daily_sales || selectedProduct.average_daily_sales || 0,
        recommendation: data.recommendation || data.advice // Backend'den gelen tavsiye
      };

      setSelectedAnalysis(formattedData);
      setIsModalOpen(true);
    } catch (error) {
      console.error("AI bağlantı hatası:", error);
      alert("Backend'e bağlanılamadı. Lütfen terminalde 'uvicorn main:app --reload' komutunun çalıştığından emin ol!");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F6F1EB]">
      <MainLayout activeTab={activeTab} setActiveTab={setActiveTab}>
        {activeTab === "dashboard" && (
          <div className="animate-in fade-in duration-700 pb-12">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-sm font-black uppercase tracking-[0.3em] text-[#847B78]">
                Featured Products
              </h2>
              <span className="text-[10px] font-bold bg-[#D98E5E]/10 text-[#D98E5E] px-4 py-1.5 rounded-full uppercase tracking-widest border border-[#D98E5E]/10">
                Live Inventory
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-10">
              {featuredProducts.map((item) => (
                <ProductCard key={item.id} {...item} highlight />
              ))}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
              <SummaryCard
                icon={<Package size={18} />}
                title="Total Products"
                value={demoProducts.length}
                subtitle="Displayed inventory items"
              />
              <SummaryCard
                icon={<TriangleAlert size={18} />}
                title="Attention Area"
                value="03"
                subtitle="Items shown in Stock Attention"
                accent="text-red-500"
              />
              <SummaryCard
                icon={<TrendingUp size={18} />}
                title="AI Support"
                value="Ready"
                subtitle="Analysis modal available"
                accent="text-emerald-600"
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
              <div className="lg:col-span-8 bg-white border border-[#E5DCD4] rounded-[3rem] p-8 shadow-sm">
                <div className="flex items-center gap-4 mb-6 text-red-600">
                  <TriangleAlert size={22} />
                  <h2 className="text-xl font-black uppercase tracking-tight text-[#1F1311]">
                    Stock Attention
                  </h2>
                </div>

                <div className="space-y-2.5">
                  {demoProducts.slice(0, 4).map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between p-4 bg-[#FAF9F7] rounded-2xl border border-[#F2EDE8]"
                    >
                      <div>
                        <span className="block font-bold text-[#1F1311] uppercase text-[10px] tracking-widest">
                          {item.name}
                        </span>
                        <span className="text-xs text-[#847B78]">
                          Unit cost: ₺{item.unit_cost}
                        </span>
                      </div>

                      <div className="text-right">
                        <span className="block font-black text-[#D98E5E] text-xs">
                          {item.current_stock} {item.unit}
                        </span>
                        <span className="text-[11px] text-[#847B78]">
                          Current stock
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="lg:col-span-4 bg-[#1F1311] rounded-[2.5rem] p-6 text-white relative overflow-hidden flex flex-col justify-center min-h-[350px]">
                <div className="absolute -top-10 -right-10 w-40 h-40 rounded-full bg-[#D98E5E]/10 blur-3xl"></div>
                <div className="absolute bottom-0 left-0 w-40 h-40 rounded-full bg-[#ffffff]/5 blur-3xl"></div>

                <div className="relative z-10">
                  <div className="flex items-center gap-3 mb-4 text-[#D98E5E]">
                    <Sparkles size={18} />
                    <h2 className="text-xs font-black uppercase tracking-[0.2em]">
                      AI Advisory
                    </h2>
                  </div>

                  <p className="text-sm font-medium text-[#AFA19E] leading-6 mb-5">
                    AI helps highlight important inventory changes and guides users
                    to product-based stock analysis.
                  </p>

                  <div className="bg-white/5 border border-white/10 rounded-xl p-3 mb-5">
                    <p className="text-[9px] uppercase tracking-[0.3em] text-[#847B78] mb-1.5">
                      Design Goal
                    </p>
                    <p className="text-sm font-bold text-white">
                      Readable AI Experience
                    </p>
                    <p className="text-xs text-[#AFA19E] mt-1 leading-5">
                      Simple layout, strong hierarchy, coffee-inspired palette.
                    </p>
                  </div>

                  <button
                    onClick={() => setActiveTab("analysis")}
                    className="w-full py-3 bg-[#D98E5E] hover:bg-[#C47D4D] text-white rounded-xl font-black text-[9px] uppercase tracking-widest transition-all shadow-md shadow-orange-950/20"
                  >
                    Open Analysis View
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "analysis" && (
          <div className="animate-in slide-in-from-right-8 duration-700 grid grid-cols-12 gap-10 items-start">
            <div className="col-span-12 xl:col-span-5 bg-white/85 border border-white backdrop-blur-xl rounded-[3rem] p-8 shadow-xl flex flex-col h-[490px]">
              <div className="flex items-center justify-between mb-6 border-b border-[#F2EDE8] pb-5">
                <h3 className="text-xs font-black uppercase tracking-[0.3em] text-[#1F1311]">
                  Product List
                </h3>
                <span className="text-[9px] font-black text-[#AFA19E] uppercase">
                  {demoProducts.length} Items
                </span>
              </div>

              <div className="flex-1 overflow-y-auto pr-2 space-y-2 custom-scrollbar">
                {demoProducts.map((item) => (
                  <ProductListItem
                    key={item.id}
                    product={item}
                    selected={selectedProductId === item.id}
                    onClick={() => setSelectedProductId(item.id)}
                  />
                ))}
              </div>
            </div>

            <div className="col-span-12 xl:col-span-7 bg-[#1F1311] rounded-[3rem] p-8 shadow-2xl relative overflow-hidden h-[490px]">
              <div className="absolute -top-20 -right-20 w-64 h-64 bg-[#D98E5E] opacity-10 blur-[100px]"></div>
              <div className="absolute bottom-0 left-0 w-48 h-48 bg-white opacity-5 blur-[120px]"></div>

              {!selectedProduct ? (
                <EmptyAnalysisState onAnalyzeClick={handleAnalyze} />
              ) : (
                <div className="relative z-10 h-full flex flex-col">

                  <div className="relative mb-6">
                    <Search
                      size={16}
                      className="absolute left-4 top-1/2 -translate-y-1/2 text-[#AFA19E]"
                    />
                    <input
                      type="text"
                      placeholder="Search product..."
                      value={productSearch}
                      onChange={(e) => setProductSearch(e.target.value)}
                      className="w-full rounded-2xl border border-white/10 bg-white/5 py-3 pl-11 pr-4 text-sm text-white outline-none focus:ring-1 focus:ring-[#D98E5E] transition-all"
                    />

                    {productSearch && (
                      <div className="absolute z-20 mt-2 w-full overflow-hidden rounded-2xl border border-white/10 bg-[#2A1D1A] shadow-2xl">
                        {filteredProducts.length > 0 ? (
                          filteredProducts.map((item) => (
                            <button
                              key={item.id}
                              onClick={() => {
                                setSelectedProductId(item.id);
                                setProductSearch("");
                              }}
                              className="w-full px-4 py-3 text-left text-sm text-white hover:bg-[#3a2722] transition"
                            >
                              {item.name}
                            </button>
                          ))
                        ) : (
                          <div className="px-4 py-3 text-sm text-[#AFA19E]">
                            No matching product found
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  <div className="flex items-start justify-between gap-6 mb-6">
                    <div>
                      <p className="text-[10px] font-black uppercase tracking-[0.35em] text-[#847B78] mb-2">
                        Selected Product
                      </p>
                      <h2 className="text-3xl font-black text-white tracking-tight leading-tight">
                        {selectedProduct.name}
                      </h2>
                    </div>

                    <span className="shrink-0 inline-flex items-center gap-2 text-[10px] font-black uppercase px-4 py-2 rounded-full border bg-[#D98E5E]/10 text-[#D98E5E] border-[#D98E5E]/20">
                      Ready
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-3 mb-6">
                    <div className="rounded-2xl bg-white/5 border border-white/10 p-4">
                      <p className="text-[10px] uppercase tracking-[0.2em] text-[#847B78] mb-1">
                        Stock
                      </p>
                      <p className="text-xl font-black text-white">
                        {selectedProduct.current_stock}
                        <span className="text-[10px] ml-1 text-[#AFA19E] uppercase font-normal">
                          {selectedProduct.unit}
                        </span>
                      </p>
                    </div>

                    <div className="rounded-2xl bg-white/5 border border-white/10 p-4">
                      <p className="text-[10px] uppercase tracking-[0.2em] text-[#847B78] mb-1">
                        Cost
                      </p>
                      <p className="text-xl font-black text-white">
                        ₺{selectedProduct.unit_cost}
                      </p>
                    </div>

                    <div className="rounded-2xl bg-white/5 border border-white/10 p-4">
                      <p className="text-[10px] uppercase tracking-[0.2em] text-[#847B78] mb-1">
                        AI
                      </p>
                      <p className="text-xl font-black text-white">Ready</p>
                    </div>
                  </div>

                  <div className="rounded-3xl bg-white/5 border border-white/10 p-5 mb-6">
                    <p className="text-[10px] font-black uppercase tracking-widest text-white/50 mb-2">
                      System Status
                    </p>
                    <p className="text-[#AFA19E] leading-relaxed text-sm">
                      AI analysis is ready for <span className="text-white font-bold">{selectedProduct.name}</span>.
                      Proceed to generate stock forecasts and optimization advice.
                    </p>
                  </div>

                  <div className="mt-auto">
                    <button
                      onClick={handleAnalyze}
                      disabled={!selectedProduct || isAnalyzing}
                      className={`w-full py-4 rounded-2xl font-black uppercase tracking-[0.3em] text-[10px] transition-all shadow-lg ${
                        selectedProduct && !isAnalyzing
                          ? "bg-[#D98E5E] hover:bg-[#C47D4D] text-white shadow-orange-950/30"
                          : "bg-[#AFA19E]/20 text-white/40 cursor-not-allowed shadow-none"
                      }`}
                    >
                      {isAnalyzing ? (
                        <span className="flex items-center justify-center gap-2">
                          <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                          Analyzing...
                        </span>
                      ) : (
                        "AI Stock Analysis"
                      )}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </MainLayout>

      <AnalysisModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        analysis={selectedAnalysis}
      />
    </div>
  );
};

export default Dashboard;