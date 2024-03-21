import { configureStore } from '@reduxjs/toolkit';
import CountryReducer from '@/redux/country';

const store = configureStore({
	reducer: {
		country: CountryReducer
	},
});

export type RootState = ReturnType<typeof store.getState>

export default store;