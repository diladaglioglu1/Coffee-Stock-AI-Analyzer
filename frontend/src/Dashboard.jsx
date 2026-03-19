import React, { useState, useEffect, useMemo } from "react";
import {
  Package,
  Truck,
  ShoppingCart,
  RefreshCcw,
  BarChart3,
  Search,
  TriangleAlert,
} from "lucide-react";

import MainLayout from "./layout/MainLayout";
import ProductCard from "./components/ProductCard";
import SummaryCard from "./components/SummaryCard";
import AnalysisModal from "./components/AnalysisModal";
import EmptyAnalysisState from "./components/EmptyAnalysisState";
import ProductListItem from "./components/ProductListItem";
import { demoProducts, demoAnalyses } from "./data/demoData";

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [products, setProducts] = useState(demoProducts);
  const [selectedProductId, setSelectedProductId] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [productSearch, setProductSearch] = useState("");
  const [uiError, setUiError] = useState("");
  const [aiStatus, setAiStatus] = useState("Ready");
  const [isDemoMode, setIsDemoMode] = useState(false);

  const supplierPreview = [
    {
      id: 1,
      name: "BeanCraft Supply",
      products: ["Espresso Beans", "House Blend Beans", "Colombia Beans"],
    },
    {
      id: 2,
      name: "MilkFlow Distributors",
      products: ["Whole Milk", "Oat Milk", "Almond Milk"],
    },
    {
      id: 3,
      name: "SweetSource Syrups",
      products: ["Caramel Syrup", "Vanilla Syrup", "Hazelnut Syrup"],
    },
  ];

  const fetchProducts = async () => {
    try {
      setUiError("");
      const response = await fetch("http://localhost:8000/api/stock/products");

      if (!response.ok) {
        throw new Error("Products request failed");
      }

      const data = await response.json();

      if (Array.isArray(data) && data.length > 0) {
        setProducts(data);
        setIsDemoMode(false);
      }
    } catch (error) {
      console.warn("Backend offline. Demo mode is active.", error);
      setProducts(demoProducts);
      setIsDemoMode(true);
      setUiError("Demo mode is active.");
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const filteredProducts = useMemo(() => {
    return products.filter((p) =>
      p.name.toLowerCase().includes(productSearch.toLowerCase())
    );
  }, [products, productSearch]);

  useEffect(() => {
    if (filteredProducts.length > 0 && !selectedProductId) {
      setSelectedProductId(filteredProducts[0].id);
      return;
    }

    const selectedStillVisible = filteredProducts.some(
      (p) => p.id === selectedProductId
    );

    if (!selectedStillVisible) {
      setSelectedProductId(filteredProducts[0]?.id ?? null);
    }
  }, [filteredProducts, selectedProductId]);

  useEffect(() => {
    setAiStatus("Ready");
    setSelectedAnalysis(null);
  }, [selectedProductId]);

  const simulateDemoDay = () => {
    const simulatedProducts = products.map((product) => {
      let reduction = 0;

      if (product.name.toLowerCase().includes("beans")) {
        reduction = Math.floor(Math.random() * 4) + 1;
      } else if (product.name.toLowerCase().includes("milk")) {
        reduction = Math.floor(Math.random() * 5) + 2;
      } else if (product.name.toLowerCase().includes("syrup")) {
        reduction = Math.floor(Math.random() * 3) + 1;
      } else if (product.name.toLowerCase().includes("matcha")) {
        reduction = Math.floor(Math.random() * 2) + 1;
      } else {
        reduction = Math.floor(Math.random() * 2) + 1;
      }

      return {
        ...product,
        current_stock: Math.max(0, product.current_stock - reduction),
      };
    });

    setProducts(simulatedProducts);
    setUiError("Running in demo mode. Actions are simulated locally.");
  };

  const handleSimulateDay = async () => {
    try {
      setUiError("");

      const response = await fetch("http://localhost:8000/api/stock/simulate-day", {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Simulation failed");
      }

      await fetchProducts();
      alert("Daily simulation completed successfully.");
    } catch (err) {
      console.warn("Simulation unavailable. Using demo simulation.", err);
      simulateDemoDay();
      alert("Demo daily simulation completed.");
    }
  };

  const selectedProduct =
    products.find((p) => p.id === selectedProductId) || null;

  const handleAnalyze = async () => {
    if (!selectedProduct) return;

    setIsAnalyzing(true);
    setAiStatus("Processing");
    setUiError("");

    try {
      const response = await fetch(
        `http://localhost:8000/api/ai/analyze/${selectedProduct.id}`
      );

      if (!response.ok) {
        throw new Error("AI analysis request failed");
      }

      const data = await response.json();

      setSelectedAnalysis({
        product_name: data.product_name || selectedProduct.name,
        advice: data.advice,
        source: data.source || "AI",
        cache_hit: data.cache_hit ?? false,
        rate_limited: data.rate_limited ?? false,
        current_stock: selectedProduct.current_stock,
        unit: selectedProduct.unit,
        unit_cost: selectedProduct.unit_cost,
      });

      setIsModalOpen(true);
      setAiStatus("Completed");
      setIsDemoMode(false);
    } catch (error) {
      console.warn("AI service unavailable. Using demo analysis.", error);

      const demoResult = demoAnalyses[selectedProduct.id];

      if (demoResult) {
        setSelectedAnalysis({
          product_name: demoResult.product_name || selectedProduct.name,
          advice: demoResult.recommendation,
          source: "Demo AI",
          cache_hit: null,
          rate_limited: false,
          current_stock: selectedProduct.current_stock,
          unit: selectedProduct.unit,
          unit_cost: selectedProduct.unit_cost,
        });

        setIsModalOpen(true);
        setAiStatus("Completed");
        setUiError(isDemoMode ? "Demo mode is active." : "");
      } else {
        setUiError("AI analysis is currently unavailable.");
        setAiStatus("Ready");
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  const beanProducts = products
    .filter((p) => p.name.toLowerCase().includes("beans"))
    .slice(0, 4);

  const wasteItems = [
    "Whole Milk (Expired)",
    "Espresso (Spillage)",
    "Oat Milk (Operational)",
    "Matcha Powder (Expired)",
    "Caramel Syrup (Leakage)",
    "Ice Cubes (Melt Loss)",
  ];

  const orderItems = [
    { label: "LOCAL DAIRY - PROCESSING", color: "border-orange-400" },
    { label: "GREEN FARM - PENDING", color: "border-blue-400" },
    { label: "SYRUP HUB - APPROVED", color: "border-violet-400" },
    { label: "MATCHA SUPPLY - REVIEW", color: "border-red-400" },
    { label: "BEANCRAFT SUPPLY - SHIPPED", color: "border-emerald-500" },
  ];

  return (
    <div className="min-h-screen bg-[#F6F1EB]">
      <MainLayout activeTab={activeTab} setActiveTab={setActiveTab}>
        {uiError && (
          <div className="mb-6 rounded-2xl border border-amber-200 bg-amber-50 px-5 py-4 text-sm font-medium text-amber-800">
            {uiError}
          </div>
        )}

        {activeTab === "dashboard" && (
          <div className="animate-in fade-in duration-700 pb-12">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-sm font-black uppercase tracking-[0.3em] text-[#847B78]">
                Operational Overview
              </h2>

              <button
                onClick={handleSimulateDay}
                className="flex items-center gap-2 text-[10px] font-black bg-[#1F1311] text-white px-5 py-2.5 rounded-full uppercase tracking-widest hover:bg-[#3A2722] transition-all shadow-md"
              >
                <RefreshCcw size={12} />
                Run Daily Simulation
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-8 mb-12">
              {beanProducts.map((item) => (
                <ProductCard key={item.id} {...item} highlight={true} />
              ))}
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 items-stretch">
              <div className="xl:col-span-4 grid grid-cols-1 gap-6 h-full">
                <SummaryCard
                  icon={<Package size={18} />}
                  title="Products"
                  value={products.length}
                  subtitle="Entity: Product Catalog"
                />

                <SummaryCard
                  icon={<BarChart3 size={18} />}
                  title="Daily Income"
                  value="₺8,420"
                  subtitle="Today’s estimated earnings"
                  accent="text-emerald-600"
                />

                <div className="bg-white border border-[#E9DED4] rounded-[2rem] p-6 shadow-sm hover:shadow-md transition-all flex flex-col h-[260px]">
                  <div className="flex items-center gap-3 mb-4 text-blue-500">
                    <Truck size={18} />
                    <span className="text-[11px] font-black uppercase tracking-[0.2em]">
                      Supplier Overview
                    </span>
                  </div>

                  <div className="flex-1 overflow-y-auto pr-2 space-y-3 custom-scrollbar">
                    {supplierPreview.map((supplier) => (
                      <div
                        key={supplier.id}
                        className="rounded-2xl border border-[#F2EDE8] bg-[#FAF9F7] px-5 py-4"
                      >
                        <p className="text-[12px] font-black uppercase tracking-wide text-[#1F1311] mb-3">
                          {supplier.name}
                        </p>

                        <div className="space-y-2">
                          {supplier.products.map((product, index) => (
                            <p
                              key={index}
                              className="text-[11px] font-bold text-[#6F6663] leading-5"
                            >
                              • {product}
                            </p>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="xl:col-span-4 bg-white border border-[#E5DCD4] rounded-[3rem] p-7 shadow-sm flex flex-col h-[480px]">
                <div className="flex items-center justify-between mb-5 shrink-0">
                  <div className="flex items-center gap-3 text-red-500">
                    <TriangleAlert size={18} />
                    <h2 className="text-[11px] font-black uppercase tracking-[0.2em] text-[#1F1311]">
                      Waste Preview
                    </h2>
                  </div>
                  <span className="text-[9px] font-black bg-red-50 text-red-600 px-3 py-1 rounded-full uppercase">
                    {wasteItems.length} Items
                  </span>
                </div>

                <div className="flex-1 overflow-y-auto pr-2 space-y-2 custom-scrollbar">
                  {wasteItems.map((item, index) => (
                    <div
                      key={index}
                      className="p-3 bg-[#FAF9F7] rounded-xl border border-[#F2EDE8] hover:border-red-100 transition-colors"
                    >
                      <p className="text-[11px] font-bold text-red-500 uppercase tracking-tight italic">
                        {item}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="xl:col-span-4 bg-white border border-[#E5DCD4] rounded-[3rem] p-7 shadow-sm flex flex-col h-[480px]">
                <div className="flex items-center justify-between mb-5 text-[#1F1311] shrink-0">
                  <div className="flex items-center gap-3">
                    <ShoppingCart size={20} />
                    <h2 className="text-[11px] font-black uppercase tracking-[0.2em]">
                      Order Preview
                    </h2>
                  </div>
                  <span className="text-[9px] font-black bg-[#D98E5E]/10 text-[#D98E5E] px-3 py-1 rounded-full uppercase">
                    {orderItems.length} Items
                  </span>
                </div>

                <div className="flex-1 overflow-y-auto pr-2 space-y-3 custom-scrollbar">
                  {orderItems.map((item, index) => (
                    <div
                      key={index}
                      className={`p-3.5 bg-[#FAF9F7] rounded-xl border-l-[4px] ${item.color} shadow-sm hover:translate-x-1 transition-transform cursor-default`}
                    >
                      <span className="text-[11px] font-black text-[#1F1311] tracking-tight">
                        {item.label}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "analysis" && (
          <div className="grid grid-cols-12 gap-10 items-start h-[560px]">
            <div className="col-span-12 xl:col-span-5 bg-white border border-[#F2EDE8] rounded-[3rem] p-8 flex flex-col h-full shadow-sm overflow-hidden">
              <div className="flex items-center justify-between mb-4 border-b border-[#FAF6F2] pb-4">
                <h3 className="text-xs font-black uppercase tracking-[0.3em] text-[#1F1311]">
                  Inventory Selector
                </h3>
                <span className="text-[9px] font-black text-[#AFA19E] uppercase">
                  {filteredProducts.length} Results
                </span>
              </div>

              <div className="flex-1 overflow-y-auto pr-2 space-y-2 custom-scrollbar">
                {filteredProducts.length > 0 ? (
                  filteredProducts.map((item) => (
                    <ProductListItem
                      key={item.id}
                      product={item}
                      selected={selectedProductId === item.id}
                      onClick={() => setSelectedProductId(item.id)}
                    />
                  ))
                ) : (
                  <div className="rounded-2xl border border-dashed border-[#E9DED4] p-6 text-center text-sm text-[#847B78]">
                    No products match your search.
                  </div>
                )}
              </div>
            </div>

            <div className="col-span-12 xl:col-span-7 bg-[#1F1311] rounded-[3rem] p-8 shadow-2xl h-[720px] xl:h-[560px] relative overflow-hidden flex flex-col">
              <div className="absolute -top-24 -right-24 w-64 h-64 bg-[#D98E5E] opacity-10 blur-[120px]"></div>

              {!selectedProduct ? (
                <EmptyAnalysisState />
              ) : (
                <div className="relative z-10 h-full flex flex-col min-h-0">
                  <div className="relative mb-5 shrink-0">
                    <Search
                      size={16}
                      className="absolute left-4 top-1/2 -translate-y-1/2 text-[#AFA19E]"
                    />
                    <input
                      type="text"
                      placeholder="Search product..."
                      value={productSearch}
                      onChange={(e) => setProductSearch(e.target.value)}
                      className="w-full rounded-2xl bg-white/5 py-3 pl-12 pr-4 text-sm text-white outline-none border border-white/10 placeholder:text-[#AFA19E] focus:border-[#D98E5E]/50 transition-all"
                    />
                  </div>

                  <div className="flex items-start justify-between gap-6 mb-5 shrink-0">
                    <div className="flex-1">
                      <p className="text-[10px] font-black uppercase tracking-[0.3em] text-[#847B78] mb-2">
                        Selected Entry
                      </p>

                      <div className="flex items-center justify-between gap-4">
                        <h2 className="text-4xl font-black text-white tracking-tighter leading-tight">
                          {selectedProduct.name}
                        </h2>

                        <span className="inline-flex items-center gap-2 text-[10px] font-black uppercase px-4 py-2 rounded-full border bg-[#D98E5E]/10 text-[#D98E5E] border-[#D98E5E]/20 shrink-0">
                          {selectedProduct.current_stock < 15 ? "Low Stock" : "Active"}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 shrink-0">
                    <div className="rounded-2xl bg-white/5 border border-white/10 p-5">
                      <p className="text-[10px] uppercase tracking-[0.25em] text-[#847B78] mb-2">
                        Real-time Stock
                      </p>
                      <p className="text-3xl font-black text-white">
                        {selectedProduct.current_stock}
                        <span className="text-sm ml-2 text-[#AFA19E] uppercase">
                          {selectedProduct.unit}
                        </span>
                      </p>
                    </div>

                    <div className="rounded-2xl bg-white/5 border border-white/10 p-5">
                      <p className="text-[10px] uppercase tracking-[0.25em] text-[#847B78] mb-2">
                        Cost Unit
                      </p>
                      <p className="text-3xl font-black text-white">
                        ₺{selectedProduct.unit_cost}
                      </p>
                    </div>

                    <div className="rounded-2xl bg-white/5 border border-white/10 p-5">
                      <p className="text-[10px] uppercase tracking-[0.25em] text-[#847B78] mb-2">
                        AI State
                      </p>
                      <p
                        className={`text-2xl font-black ${
                          aiStatus === "Processing"
                            ? "text-yellow-400"
                            : aiStatus === "Completed"
                            ? "text-green-400"
                            : "text-white"
                        }`}
                      >
                        {aiStatus}
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 flex-1 min-h-0">
                    <div className="rounded-2xl bg-white/5 border border-white/10 p-5">
                      <p className="text-[10px] uppercase tracking-[0.25em] text-[#847B78] mb-2">
                        Stock Status
                      </p>
                      <p className="text-xl font-black text-white mb-3">
                        {selectedProduct.current_stock < 10
                          ? "Critical"
                          : selectedProduct.current_stock < 15
                          ? "Monitor"
                          : "Healthy"}
                      </p>
                      <p className="text-xs text-[#AFA19E] leading-7">
                        {selectedProduct.current_stock < 10
                          ? "This item is close to depletion and should be reviewed immediately."
                          : selectedProduct.current_stock < 15
                          ? "This item is within warning range and should be monitored."
                          : "Current stock level appears stable for short-term operations."}
                      </p>
                    </div>

                    <div className="rounded-2xl bg-white/5 border border-white/10 p-5">
                      <p className="text-[10px] uppercase tracking-[0.25em] text-[#847B78] mb-2">
                        AI Action Hint
                      </p>
                      <p className="text-xl font-black text-white mb-3">
                        {selectedProduct.current_stock < 10 ? "Urgent Review" : "Run Analysis"}
                      </p>
                      <p className="text-xs text-[#AFA19E] leading-7">
                        Use the AI optimization action below to generate a smart stock recommendation for this selected product.
                      </p>
                    </div>
                  </div>

                  <div className="shrink-0 pt-2">
                    <button
                      onClick={handleAnalyze}
                      disabled={!selectedProduct || isAnalyzing}
                      className={`w-full py-3 rounded-xl font-black uppercase tracking-[0.14em] text-[9px] transition-all shadow-lg ${
                        selectedProduct && !isAnalyzing
                          ? "bg-[#D98E5E] hover:bg-[#C47D4D] text-white"
                          : "bg-white/5 text-white/40 cursor-not-allowed shadow-none"
                      }`}
                    >
                      {isAnalyzing ? "Requesting AI..." : "AI Stock Analysis"}
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