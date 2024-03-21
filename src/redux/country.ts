import { RootState } from '@/redux/store';
import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export interface Country {
	fetching: boolean,
	page: number,
	pageCount: number,
	search: string,
    sortOrder: string,
	matched: any[]
}

const initialState: Country = {
    fetching: true,
	page: 1,
	pageCount: 0,
	search: '',
	sortOrder: 'asc',
	matched: []
}

const countrySlice = createSlice({
	name: 'country',
	initialState,
	reducers: {
		changeFetching(state: Country, action: PayloadAction<boolean>) {
			state.fetching = action.payload;
		},
		changePage(state: Country, action: PayloadAction<number>) {
			state.page = action.payload;
		},
		changePageCount(state: Country, action: PayloadAction<number>) {
			state.pageCount = action.payload;
		},
		changeSearch(state: Country, action: PayloadAction<string>) {
			state.search = action.payload;
		},
		changeSortOrder(state: Country, action: PayloadAction<string>) {
			state.sortOrder = action.payload;
		},
		changeMatched(state: Country, action: PayloadAction<any[]>) {
			state.matched = action.payload;
		}
	},
});

export const CountryActions = countrySlice.actions;

export const CountrySelectors = {
	fetching: (state: RootState) => state.country.fetching,
	page: (state: RootState) => state.country.page,
	pageCount: (state: RootState) => state.country.pageCount,
	search: (state: RootState) => state.country.search,
	sortOrder: (state: RootState) => state.country.sortOrder,
	matched: (state: RootState) => state.country.matched,
}

export default countrySlice.reducer;