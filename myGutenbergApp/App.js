import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, View, ScrollView } from 'react-native';
import BackgroundImage from './public/smoky-background.png';
import SearchBar from './src/components/search-bar';
import BooksMasonry from './src/components/masonry';

export default function App() {
	return (
		<View style={styles.container}>
			<SearchBar />
			<ScrollView contentContainerStyle={styles.test}>
				<BooksMasonry />
			</ScrollView>
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		backgroundImage: `url(${BackgroundImage})`,
	},
	test: {
		height: window.innerHeight,
	},
});
