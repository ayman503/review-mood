import gradio as gr
LEXICON = {'Good': 2, 'great': 2, 'excellent': 3, 'bad': -2, 'terrible': -3, 'poor': -2, 'average': 0,'love': 3, 'hate': -3, 'happy': 2, 'sad': -2, 'amazing': 3, 'awful': -3, 'fantastic': 3, 'disappointing': -2}
NEGATIONS = {'not', 'no', 'never', 'none', 'nobody', 'nothing', 'neither', 'nowhere', 'hardly', 'scarcely', 'barely'}
def analyse(review):
    pairs = []
    negate = False
    for orinigal in review.split():
        word = orinigal.lower().strip('.,!?')
        points = 0
        if word in NEGATIONS:
            negate = True
            pairs.append((orinigal, 0))
            continue
        if word in LEXICON:
            points = LEXICON[word]
            if negate:
                points = -points
                negate = False
        pairs.append((orinigal, points))
    return pairs
def check(review):
    score = sum(p for _, p in analyse(review))
    mood = 'POSITIVE' if score >=1 else ('NEGATIVE' if score <= -1 else 'NEUTRAL')
    pieces = []
    for word, points in analyse(review):
        label = 'positive' if points > 0 else ('negative' if points < 0 else None)
        pieces.append((word + " ", label))
    return score, mood, pieces
demo = gr.Interface(
    fn=check,
    inputs=gr.Textbox(label="Enter your review"),
    outputs=[
        gr.Textbox(label="Score"),
        gr.Textbox(label="Mood"),
        gr.HighlightedText(label="Analysis")
    ],
    title="Sentiment Analysis",
    description="This app analyzes the sentiment of a given review and provides a score, mood, and word-level analysis."
)
if __name__ == "__main__":
    demo.launch()