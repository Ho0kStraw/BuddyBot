
# -----------------------------
# /webcam command
# -----------------------------
@bot.tree.command(name="webcam", description="Maak één webcamfoto (demo)")
async def webcam(interaction: discord.Interaction):
    await interaction.response.defer()

    def capture_image():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False

        success, frame = cap.read()
        if success:
            cv2.imwrite("webcam.png", frame)

        cap.release()
        return success

    loop = asyncio.get_running_loop()
    success = await loop.run_in_executor(None, capture_image)

    if not success:
        await interaction.followup.send("❌ Webcam kon niet worden gebruikt.")
        return

    with open("webcam.png", "rb") as f:
        await interaction.followup.send(file=discord.File(f))

    os.remove("webcam.png")

bot.run(DISCORD_TOKEN)

