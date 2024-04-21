import { createI18n } from 'vue-i18n'
import zh from './lang/zh';
import en from './lang/en';

export const i18n = createI18n({
    // something vue-i18n options here ...
    legacy: false, // you must set `false`, to use Composition API
    locale: 'zh', // set locale
    fallbackLocale: 'en', // set fallback locale
    globalInjection: true,
    allowComposition:true,
    messages: {
        zh,
        en
    }, // set locale messages
    silentTranslationWarn:true,
    // missingWarn:false,
    // silentFallbackWarn:true,
    // fallbackWarn:false
})

