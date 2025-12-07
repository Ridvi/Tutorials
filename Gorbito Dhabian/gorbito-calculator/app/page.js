"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

// -----------------------------
// QUESTIONS DATA
// -----------------------------
const questions = [
  { q: "আপনি কেন ঢাবি লোগো বিশিষ্ট জার্সি পড়েন?", o: ["পড়ি না", "ভালো লাগে তাই", "পটানোর জন্য", "এলাকায় নিজেকে ঢাবিয়ান প্রমান করার জন্য"], s: [0, 10, 20, 30] },
  { q: "ভার্সিটি আসলে কি নিয়ে একসাইটেড থাকেন?", o: ["লেকচারা এটেন্ড", "বন্ধুদের সাথে হাহা হিহি", "ব্যাচের গেঞ্জাম", "স্বপ্নের লাল বাসে চড়া"], s: [0, 10, 20, 30] },
  { q: "জীবনের প্রথম প্রেম?", o: ["বয়েট", "প্রেমে পড়িনি", "সে", "ঢাবিই জীবন, ঢাবিই মরণ"], s: [0, 10, 20, 30] },
  { q: "কেন ঢাবিতে ভর্তি হয়েছেন?", o: ["এমনি এমনি", "কোথাও চান্স পাইনি তাই", "বিসিএস দিবো তাই", "DU is a brand, man of smart people"], s: [0, 10, 20, 30] },
  { q: "অফিসিয়াল নোটিস পাওয়ার পর আপনি কি করেন?", o: ["আই ডোন্ট কেয়ার", "কি হচ্ছে কিছু বুঝি না", "যা করেছে ভালোর জন্যই করেছে", "শিক্ষার্থী সংসদে প্রতিবাদ করেন"], s: [0, 10, 20, 30] },
  { q: "ঢাবি কি?", o: ["বিশ্ববিদ্যালয়", "জেলখানা", "বাসস্ট্যান্ড", "পার্ক"], s: [0, 10, 20, 30] },
  { q: "ঢাবি থেকে উদ্যান সরানো উচিত নাকি উদ্যান থেকে ঢাবি?", o: ["উদ্যানকে", "আমি সুশীল", "শাহবাগকে", "ঢাবিকে"], s: [0, 10, 20, 30] },
  { q: "ঢাবি কোন ধরনের প্রতিষ্ঠান?", o: ["জ্বালাময়ী", "অত্যাচারী", "রাজনৈতিক", "স্বৈরাচারী"], s: [0, 10, 20, 30] },
  { q: "আপনার হল কোনটি?", o: ["হলে থাকি না", "আপনি শুনে কি করবেন?", "উদ্যানে থাকি", "কার্জন হল"], s: [0, 10, 20, 30] },
  { q: "দেশে কোনো সমস্যা হলে, আপনি কি করেন?", o: ["কোনো খবর রাখি না", "সমস্যার সমাধান বের করি", "সুশীলগিরি করি", "ঢাবিকে দোষ দেই"], s: [0, 10, 20, 30] },
  { q: "ঢাবি কে প্রাচ্যের অক্সফোর্ড বলা হয় কেন?", o: ["অনেক রিসার্চ হয়", "ঢাবির সামনে অক্সফোর্ড কিছুই না", "বিসিএস এ সেরা পারফরমেন্স", "রাজনৈতিক চেতনা"], s: [0, 10, 20, 30] },
  { q: "ঢাবিতে ভর্তি হওয়ার পর আপনার দাবি দাওয়া পেশ করেন?", o: ["আমার কোনো দাবি নেই", "বাবা মার কাছে", "সংসদে", "রাজুতে"], s: [0, 10, 20, 30] },
  { q: "Xibir সম্পর্কে সঠিক কোনটি?", o: ["সাধারণ শিক্ষার্থী", "গুপ্ত", "ঢাবির সব Xibir, আমি আমার বিবির", "মানুষ মূলত Xibir"], s: [0, 10, 20, 30] },
  { q: "ঢাবিতে চান্স পাওয়া থেকে ভর্তি কঠিন?", o: ["একমত হতে পারছি না", "চান্সই পাই নি", "আমি অনেক চালাক, একদিনে করে ফেলছি", "সহমত"], s: [0, 10, 20, 30] },
  { q: "আপনি কি কার্জনে ছবি তুলেছেন?", o: ["পড়াশোনার চাপে বাঁচিনা", "অন্যের ছবি তোলা দেখি", "এইটা পরীক্ষার হল, শুটিং স্পট না", "কার্জনের প্রত্যেক কোনায় ছবি তুলেছি"], s: [0, 10, 20, 30] },
  { q: "ধাবি খাবারের প্রতি আপনার মতামত?", o: ["মোটামুটি", "ভালো", "খুব ভালো", "Michelin star"], s: [0, 10, 20, 30] },
  { q: "Final exam এর প্রশ্ন দেখে?", o: ["টেনশন", "Solve try", "manageable", "ধাবিয়ানকে চ্যালেঞ্জ? অসম্ভব!"], s: [0, 10, 20, 30] },
  { q: "রাতে group study?", o: ["না", "কখনো", "হয়", "আমরা ৪টা পর্যন্ত discuss করি"], s: [0, 10, 20, 30] },
  { q: "ফ্রি পিরিয়ডে কী করেন?", o: ["ঘুম", "চা", "walk", "ধাবি ঘুরি"], s: [0, 10, 20, 30] },
  { q: "আপনি নিজেকে কিভাবে describe করেন?", o: ["Student", "Regular", "Dedicated", "গর্বের walking logo"], s: [0, 10, 20, 30] }
];

// -----------------------------
// SVG ICONS
// -----------------------------
const Icons = {
  Share: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
  ),
  Restart: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2.5 2v6h6"/><path d="M21.5 22v-6h-6"/><path d="M22 11.5A10 10 0 0 0 3.2 7.2M2 12.5a10 10 0 0 0 18.8 4.2"/></svg>
  ),
  Check: () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
  )
};

// -----------------------------
// MAIN COMPONENT
// -----------------------------
export default function GorbitoCalculator() {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [isFinished, setIsFinished] = useState(false);
  const [scoreData, setScoreData] = useState(null);

  // Handle Option Click
  const handleOptionSelect = (score) => {
    // Record answer
    const newAnswers = { ...answers, [currentStep]: score };
    setAnswers(newAnswers);

    // Delay slightly for visual feedback before moving next
    setTimeout(() => {
      if (currentStep < questions.length - 1) {
        setCurrentStep(currentStep + 1);
      } else {
        calculateResult(newAnswers);
      }
    }, 250);
  };

  // Calculate Logic
  const calculateResult = (finalAnswers) => {
    const total = Object.values(finalAnswers).reduce((a, b) => a + b, 0);
    const max = questions.length * 30;
    const p = Math.round((total / max) * 100);

    let cat = "";
    let color = "";
    
    if (p < 45) {
      cat = "আগে ছান্স পেয়ে দেখাও!🫶";
      color = "text-red-500";
    } else if (p < 60) {
      cat = "আরো প্রতিবাদী হতে হবে, আওয়াজ তোলা শিখুন ✊";
      color = "text-yellow-600";
    } else if (p < 85) {
      cat = "ছান্স কনফার্ম। এখন বের হয়ে দেখাও 😊";
      color = "text-blue-600";
    } else {
      cat = "🔥 আপনি গর্বে গর্ভবতী। তো কত মাস চলে???";
      color = "text-purple-600";
    }

    // Set Data FIRST, then finish
    const resultData = { p, cat, color };
    setScoreData(resultData);
    setIsFinished(true);
  };

  // Share Logic
  const handleShare = async () => {
    // Safety check: if data isn't ready, don't run
    if (!scoreData) return;

    const text = `আমি গর্বিত ঢাবিয়ান ক্যালকুলেটরে ${scoreData.p}% স্কোর করেছি! ${scoreData.cat}`;
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Gorbito Dhabian Calculator',
          text: text,
          url: window.location.href,
        });
      } catch (err) {
        console.log('Share canceled');
      }
    } else {
      navigator.clipboard.writeText(`${text} ${window.location.href}`);
      alert("রেজাল্ট কপি করা হয়েছে! বন্ধুদের সাথে শেয়ার করুন।");
    }
  };

  // Calculate Progress
  const progress = ((currentStep) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4 font-sans selection:bg-blue-100 selection:text-blue-900">
      
      {/* Background Decorative Blobs */}
      <div className="fixed top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
        <div className="absolute top-[-10%] right-[-10%] w-96 h-96 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-[-20%] left-[20%] w-96 h-96 bg-pink-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>
      </div>

      <div className="w-full max-w-2xl">
        
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-3xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-purple-600 tracking-tight">
            Gorbito Dhabian
          </h1>
          <p className="text-slate-500 mt-2 font-medium tracking-wide">CALCULATOR</p>
        </motion.div>

        {/* Main Card */}
        <motion.div 
          className="bg-white/80 backdrop-blur-xl border border-white/20 shadow-2xl rounded-3xl overflow-hidden relative"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.4 }}
        >
          
          {/* Progress Bar (Only visible during quiz) */}
          {!isFinished && (
            <div className="h-2 w-full bg-slate-100">
              <motion.div 
                className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          )}

          <div className="p-6 md:p-10 min-h-[400px] flex flex-col justify-center">
            <AnimatePresence mode="wait">
              
              {/* LOGIC FIX: Check !isFinished OR if scoreData is null */}
              {!isFinished ? (
                /* ---------------- QUESTION VIEW ---------------- */
                <motion.div
                  key={currentStep}
                  initial={{ x: 50, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: -50, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="w-full"
                >
                  <div className="flex justify-between items-center mb-6 text-sm font-bold text-slate-400 uppercase tracking-widest">
                    <span>Question {currentStep + 1}</span>
                    {/*<span>{questions.length} Total</span>*/}
                  </div>

                  <h2 className="text-2xl md:text-3xl font-bold text-slate-800 mb-8 leading-snug">
                    {questions[currentStep].q}
                  </h2>

                  <div className="grid grid-cols-1 gap-3">
                    {questions[currentStep].o.map((option, idx) => (
                      <motion.button
                        key={idx}
                        whileHover={{ scale: 1.02, backgroundColor: "rgba(59, 130, 246, 0.05)" }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => handleOptionSelect(questions[currentStep].s[idx])}
                        className="group flex items-center justify-between w-full p-5 text-left border border-slate-200 rounded-xl hover:border-blue-400 hover:shadow-md transition-all duration-200 bg-white"
                      >
                        <span className="text-lg font-medium text-slate-700 group-hover:text-blue-700 transition-colors">
                          {option}
                        </span>
                        <div className="w-5 h-5 rounded-full border-2 border-slate-300 group-hover:border-blue-500 flex items-center justify-center">
                          <div className="w-2.5 h-2.5 rounded-full bg-blue-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                        </div>
                      </motion.button>
                    ))}
                  </div>
                </motion.div>
              ) : (
                /* ---------------- RESULT VIEW ---------------- */
                /* LOGIC FIX: Added scoreData && to ensure it exists before rendering */
                scoreData && (
                  <motion.div
                    key="result"
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="text-center w-full"
                  >
                    <div className="w-24 h-24 bg-gradient-to-tr from-blue-500 to-purple-500 rounded-full mx-auto flex items-center justify-center mb-6 shadow-lg shadow-blue-200">
                      <Icons.Check />
                    </div>
                    
                    <h2 className="text-lg font-semibold text-slate-500 mb-2">আপনার স্কোর</h2>
                    <h1 className={`text-6xl md:text-7xl font-black ${scoreData.color} mb-6 tracking-tighter`}>
                      {scoreData.p}%
                    </h1>
                    
                    <p className="text-xl md:text-2xl text-slate-800 font-medium mb-10 px-4">
                      {scoreData.cat}
                    </p>

                    <div className="flex flex-col md:flex-row gap-4 justify-center">
                      <button
                        onClick={handleShare}
                        className="flex items-center justify-center gap-2 px-8 py-4 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 transition shadow-lg hover:shadow-xl active:scale-95"
                      >
                        <Icons.Share />
                        Share Result
                      </button>
                      
                      <button
                        onClick={() => window.location.reload()}
                        className="flex items-center justify-center gap-2 px-8 py-4 bg-white text-slate-700 border border-slate-200 rounded-xl font-bold hover:bg-slate-50 transition active:scale-95"
                      >
                        <Icons.Restart />
                        Start Again
                      </button>
                    </div>
                  </motion.div>
                )
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        <p className="text-center text-slate-400 text-sm mt-8">
            Made for fun • @Ridvi
        </p>
      </div>
    </div>
  );
}