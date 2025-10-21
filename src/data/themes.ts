export interface ThemeOption {
  id: string;
  label: string;
  colorScheme: 'light' | 'dark';
}

export const themeOptions: ThemeOption[] = [
  {
    id: 'terminal',
    label: 'Terminal',
    colorScheme: 'dark'
  },
  {
    id: 'halloween',
    label: 'Halloween',
    colorScheme: 'dark'
  },
  {
    id: 'holiday',
    label: 'Holiday',
    colorScheme: 'dark'
  },
  {
    id: 'pain',
    label: 'Pain',
    colorScheme: 'light'
  }
];

export const themeStorageKey = 'site-theme';

export const themeAliases: Record<string, string> = {
  'april-fools': 'pain'
};
