const $ = (id) => document.getElementById(id);
const patientIdKey = "ppd-ews-patient-id";
const historyKey = "ppd-ews-daily-history";
const epdsRiskKey = "ppd-ews-latest-epds-risk";
let weeklyAssessmentDue = false;
const productionMode = $("production-mode");

function patientId() {
  let id = localStorage.getItem(patientIdKey);
  if (!id) { id = crypto.randomUUID?.() || `browser-${Date.now()}`; localStorage.setItem(patientIdKey, id); }
  return id;
}
function todayIsoDate() { return new Date(Date.now() - new Date().getTimezoneOffset() * 60_000).toISOString().slice(0, 10); }
function storedHistory() {
  try { return JSON.parse(localStorage.getItem(historyKey) || "[]").slice(-6); }
  catch { return []; }
}
function saveDailySummary(result) {
  const history = storedHistory();
  history.push({ emotion: result.emotion, depression: result.depression, behavior_count: result.behaviors.length, epds_risk: result.epds });
  localStorage.setItem(historyKey, JSON.stringify(history.slice(-6)));
  localStorage.setItem(epdsRiskKey, result.epds);
}
function apiErrorMessage(detail) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map((item) => item.msg || "Invalid form data.").join(" ");
  return "Could not complete the assessment. Please try again.";
}

const epdsQuestions = [
  ["I have been able to laugh and see the funny side of things", ["As much as I always could", "Not quite so much now", "Definitely not so much now", "Not at all"]],
  ["I have looked forward with enjoyment to things", ["As much as I ever did", "Rather less than I used to", "Definitely less than I used to", "Hardly at all"]],
  ["I have blamed myself unnecessarily when things went wrong", ["Yes, most of the time", "Yes, some of the time", "Not very often", "No, never"]],
  ["I have been anxious or worried for no good reason", ["No, not at all", "Hardly ever", "Yes, sometimes", "Yes, very often"]],
  ["I have felt scared or panicky for no very good reason", ["Yes, quite a lot", "Yes, sometimes", "No, not much", "No, not at all"]],
  ["Things have been getting on top of me", ["Yes, most of the time I haven't been able to cope at all", "Yes, sometimes I haven't been coping as well as usual", "No, most of the time I have coped quite well", "No, I have been coping as well as ever"]],
  ["I have been so unhappy that I have had difficulty sleeping", ["Yes, most of the time", "Yes, sometimes", "Not very often", "No, not at all"]],
  ["I have felt sad or miserable", ["Yes, most of the time", "Yes, quite often", "Not very often", "No, not at all"]],
  ["I have been so unhappy that I have been crying", ["Yes, most of the time", "Yes, quite often", "Only occasionally", "No, never"]],
  ["The thought of harming myself has occurred to me", ["Yes, quite often", "Sometimes", "Hardly ever", "Never"]],
];

$("epds").innerHTML = epdsQuestions.map(([question, options], index) => `<fieldset class="question"><legend><b>${index + 1}.</b> ${question}</legend><div class="options">${options.map((option, value) => `<label><input required type="radio" name="epds-${index}" value="${value}"><span>${option}</span></label>`).join("")}</div></fieldset>`).join("");

async function loadAssessmentStatus() {
  if (!productionMode.checked) {
    weeklyAssessmentDue = true;
    $("weekly-assessment").hidden = false;
    $("weekly-submit").hidden = false;
    $("schedule-title").textContent = "Demo mode: questions are always available";
    $("schedule-message").textContent = "Use the journal-only button for a report without EPDS answers, or complete the 10 questions and create a combined report whenever you want.";
    return;
  }
  try {
    const response = await fetch(`/epds-status/${encodeURIComponent(patientId())}`);
    const status = await response.json();
    weeklyAssessmentDue = Boolean(status.epds_due);
    $("weekly-assessment").hidden = !weeklyAssessmentDue;
    $("weekly-submit").hidden = !weeklyAssessmentDue;
    if (weeklyAssessmentDue) {
      $("schedule-title").textContent = "Your weekly questions are ready";
      $("schedule-message").textContent = "Please complete the 10 EPDS questions above. They will not appear again until seven days after submission.";
      $("submit-label").textContent = "Create weekly combined summary";
    } else {
      const due = new Date(`${status.next_epds_assessment_due}T00:00:00`).toLocaleDateString(undefined, { month: "long", day: "numeric" });
      $("schedule-title").textContent = "Your daily check-in is ready";
      $("schedule-message").textContent = `Your next weekly EPDS questions are due on ${due}. Today’s report will still use your journal and recent check-ins.`;
    }
  } catch {
    weeklyAssessmentDue = false;
    $("weekly-assessment").hidden = true;
    $("weekly-submit").hidden = true;
    $("schedule-message").textContent = "Your daily journal is ready. The weekly question schedule could not be checked, but you can still create a journal-based report.";
  }
}

const voiceButton = $("voice-journal"), voiceStatus = $("voice-status");
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
if (SpeechRecognition && !isSafari) {
  const recognition = new SpeechRecognition(); recognition.continuous = true; recognition.interimResults = true; recognition.lang = navigator.language || "en-US";
  let baseText = "", listening = false;
  voiceButton.addEventListener("click", async () => {
    if (listening) { recognition.stop(); return; }
    try { const stream = await navigator.mediaDevices.getUserMedia({ audio: true }); stream.getTracks().forEach((track) => track.stop()); baseText = $("journal").value.trim(); recognition.start(); }
    catch { voiceStatus.textContent = "Microphone access is needed for voice journaling. Allow it in browser settings and try again."; }
  });
  recognition.onstart = () => { listening = true; voiceButton.classList.add("listening"); voiceButton.textContent = "■ Stop recording"; voiceStatus.textContent = "Listening… speak naturally."; };
  recognition.onresult = (event) => { let finalText = "", interimText = ""; for (let i = 0; i < event.results.length; i++) event.results[i].isFinal ? finalText += event.results[i][0].transcript : interimText += event.results[i][0].transcript; $("journal").value = [baseText, finalText, interimText].filter(Boolean).join(" "); };
  recognition.onend = () => { listening = false; voiceButton.classList.remove("listening"); voiceButton.textContent = "🎙 Continue voice journal"; voiceStatus.textContent = "Voice entry paused. You can continue or edit the text."; };
  recognition.onerror = () => { voiceStatus.textContent = "Voice transcription could not start. Please use Chrome or type your entry."; };
} else { voiceButton.disabled = true; voiceButton.textContent = isSafari ? "Voice journal works in Chrome" : "Voice journal unavailable"; voiceStatus.textContent = isSafari ? "Use Chrome for voice transcription, or macOS Dictation in this text box." : "You can still type your entry."; }

async function submitAssessment(kind) {
  if (!$("assessment-form").reportValidity()) return;
  const button = kind === "weekly" ? $("weekly-submit") : $("daily-submit");
  const endpoint = kind === "weekly" ? "/analyze" : "/daily-check-in";
  const base = {
    patient_id: patientId(),
    doctor_email: $("doctor-email").value.trim(),
    doctor_alert_consent: $("doctor-consent").checked,
    journal: $("journal").value,
    history: storedHistory(),
  };
  const payload = kind === "weekly"
    ? { ...base, assessment_date: todayIsoDate(), enforce_weekly_schedule: productionMode.checked, epds_answers: Object.fromEntries(epdsQuestions.map((_, index) => [index + 1, Number(document.querySelector(`input[name="epds-${index}"]:checked`).value)])) }
    : { ...base, check_in_date: todayIsoDate(), latest_epds_risk: localStorage.getItem(epdsRiskKey) || "Low" };
  button.disabled = true; button.innerHTML = "Creating your summary <b>…</b>";
  try {
    const response = await fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    const data = await response.json();
    if (!response.ok) throw new Error(apiErrorMessage(data.detail));
    saveDailySummary(data); showResult(data); await loadAssessmentStatus();
  } catch (error) { $("result").hidden = false; $("result").innerHTML = `<h2>We couldn't complete your summary</h2><p>${error.message}</p>`; }
  finally { button.disabled = false; button.innerHTML = `<span>${kind === "weekly" ? "Create combined EPDS summary" : "Create journal-only summary"}</span><b>→</b>`; }
}

$("assessment-form").addEventListener("submit", (event) => { event.preventDefault(); submitAssessment("weekly"); });
$("daily-submit").addEventListener("click", () => submitAssessment("daily"));
productionMode.addEventListener("change", loadAssessmentStatus);

function showResult(data) {
  const list = (items) => `<ul>${items.map((item) => `<li>${item}</li>`).join("")}</ul>`;
  $("result").hidden = false; $("result").scrollIntoView({ behavior: "smooth", block: "start" });
  const alert = data.overall_risk === "Critical" ? `<p class="alert-status ${data.critical_alert_sent ? "sent" : "not-sent"}">${data.critical_alert_message}</p>` : "";
  $("result").innerHTML = `<div class="result-card"><p class="section-kicker">YOUR WELLBEING SUMMARY</p><h2>${data.summary}</h2><p class="risk risk-${data.overall_risk.toLowerCase()}">${data.overall_risk} early-warning level</p>${alert}<div class="result-stats"><span><b>${data.emotion}</b> emotional state</span><span><b>${data.epds}</b> latest EPDS risk</span><span><b>${Math.round(data.confidence * 100)}%</b> score-derived confidence</span></div><h3>What contributed to this result</h3><pre>${data.explanation}</pre><h3>Supportive next steps</h3>${list(data.recommendations)}<p class="next-due">Next EPDS questions due: <b>${new Date(`${data.next_epds_assessment_due}T00:00:00`).toLocaleDateString()}</b></p></div>`;
}
loadAssessmentStatus();
