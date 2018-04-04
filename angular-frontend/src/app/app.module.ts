import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';


import {AppComponent} from './app.component';
import {HeaderComponent} from './header/header.component';
import {ContentComponent} from './content/content.component';
import {SearchPageComponent} from './content/search-page/search-page.component';
import {SearchFilterComponent} from './content/search-page/search-filter/search-filter.component';
import {SearchResultsComponent} from './content/search-page/search-results/search-results.component';


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    ContentComponent,
    SearchPageComponent,
    SearchFilterComponent,
    SearchResultsComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
