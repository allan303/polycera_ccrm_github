import { createI18n } from 'vue-i18n/index'
import zh from './lang/zh';
import en from './lang/en';

export const i18n = createI18n({
    // something vue-i18n options here ...
    legacy: false, // you must set `false`, to use Composition API
    locale: 'zh', // set locale
    fallbackLocale: 'en', // set fallback locale
    globalInjection: true,
    messages: {
        zh,
        en
    }, // set locale messages
})

