document.addEventListener("DOMContentLoaded", () => {
  const textarea = document.querySelector("textarea");

  if (!textarea) {
    console.error("Textarea not found");
    return;
  }

  textarea.value = `BREAKING NEWS:

Government of India has clarified that there is NO nationwide internet shutdown.

Officials stated that viral social media claims are false and misleading.
No official directive has been issued.

Source: Press Information Bureau (PIB), Government of India`;
});
