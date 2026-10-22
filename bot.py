import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ------------------ CONTENT (all data lives here) ------------------
RULES = {
    "offside": (
        "Offside Rule",
        "A player is offside if they are closer to the opponent's goal line than both "
        "the ball and the second-last opponent when the ball is played to them, unless "
        "they are in their own half or level with the second-last opponent. Offside "
        "position is only an offence if the player becomes involved in active play."
    ),
    "fouls": (
        "Fouls & Misconduct",
        "A foul is committed when a player commits an offence against an opponent while "
        "the ball is in play, such as kicking, tripping, pushing, or tackling carelessly, "
        "recklessly, or with excessive force. A direct free kick is awarded for most fouls."
    ),
    "cards": (
        "Yellow & Red Cards",
        "A yellow card is a caution for offences like unsporting behaviour, dissent, or "
        "delaying the restart. A red card is a dismissal for serious foul play, violent "
        "conduct, or denying an obvious goal-scoring opportunity. Two yellows in one "
        "match mean a red card."
    ),
}

TEAMS = {
    "example-united": (
        "Example United",
        "League: Sample Premier League\nStadium: Example Park\n\n"
        "Fictional club used for demonstration. Founded in 1901, red and white colours, "
        "strong youth academy."
    ),
    "demo-city": (
        "Demo City",
        "League: Sample Premier League\nStadium: Demo Arena\n\n"
        "Fictional club known for attacking football. Sample data for demonstration."
    ),
}

FIXTURES = [
    "Example United vs Demo City — Sample Premier League — Saturday 15:00",
    "Demo City vs Example United — Sample Cup — Wednesday 19:45",
]

STATS = {
    "xg": (
        "Expected Goals (xG)",
        "xG measures the quality of a scoring chance. Each shot gets a value between 0 "
        "and 1 based on distance, angle, and other factors. Higher xG means a more likely "
        "goal. It compares performance beyond just goals scored."
    ),
    "possession": (
        "Possession %",
        "Possession percentage shows how much each team controlled the ball. It is the "
        "team's ball time divided by total ball-in-play time. High possession does not "
        "automatically mean a better performance."
    ),
    "ppda": (
        "PPDA (Passes Per Defensive Action)",
        "PPDA measures pressing intensity. It divides the opponent's passes by your "
        "team's defensive actions (tackles, interceptions, fouls). A lower PPDA means "
        "more aggressive pressing."
    ),
}

# ------------------ KEYBOARDS ------------------
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Rules", callback_data="menu:rules")],
        [InlineKeyboardButton("🛡️ Teams", callback_data="menu:teams")],
        [InlineKeyboardButton("📅 Fixtures", callback_data="menu:fixtures")],
        [InlineKeyboardButton("📊 Stats", callback_data="menu:stats")],
    ])

def sub_menu(kind, items):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(label, callback_data=f"{kind}:{key}")]
        for key, (label, _) in items.items()
    ])

# ------------------ HANDLERS ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⚽ Welcome to SB24GZ Football Guide!\n\n"
        "Use the menu below or these commands:\n"
        "/rules – Football rules\n"
        "/teams – Team profiles\n"
        "/fixtures – Upcoming fixtures\n"
        "/stats – Match statistics explained"
    )
    await update.message.reply_text(text, reply_markup=main_menu())

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Choose a rule:", reply_markup=sub_menu("rule", RULES))

async def teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Choose a team:", reply_markup=sub_menu("team", TEAMS))

async def fixtures(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Upcoming fixtures:\n\n" + "\n\n".join(FIXTURES))

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Choose a statistic:", reply_markup=sub_menu("stat", STATS))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "menu:rules":
        await q.edit_message_text("Choose a rule:", reply_markup=sub_menu("rule", RULES))
    elif data == "menu:teams":
        await q.edit_message_text("Choose a team:", reply_markup=sub_menu("team", TEAMS))
    elif data == "menu:fixtures":
        await q.edit_message_text("📅 Upcoming fixtures:\n\n" + "\n\n".join(FIXTURES))
    elif data == "menu:stats":
        await q.edit_message_text("Choose a statistic:", reply_markup=sub_menu("stat", STATS))
    elif data.startswith("rule:"):
        key = data.split(":")[1]
        title, body = RULES[key]
        await q.edit_message_text(f"📖 {title}\n\n{body}")
    elif data.startswith("team:"):
        key = data.split(":")[1]
        title, body = TEAMS[key]
        await q.edit_message_text(f"🛡️ {title}\n\n{body}")
    elif data.startswith("stat:"):
        key = data.split(":")[1]
        title, body = STATS[key]
        await q.edit_message_text(f"📊 {title}\n\n{body}")

# ------------------ MAIN ------------------
def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is required.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("teams", teams))
    app.add_handler(CommandHandler("fixtures", fixtures))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button))

    logging.info("Starting polling mode (Background Worker).")
    app.run_polling()

if __name__ == "__main__":
    main()
