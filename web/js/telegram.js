const tg = window.Telegram
    ?.WebApp;

if (tg) {

    tg.ready();

    tg.expand();

    console.log(
        tg.initDataUnsafe
    );
}
