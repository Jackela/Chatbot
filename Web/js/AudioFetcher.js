async function fetchAndPlayAudio(url) {
    const response = await fetch(url);
    const audioBlob = await response.blob();

    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
}

export { fetchAndPlayAudio };
