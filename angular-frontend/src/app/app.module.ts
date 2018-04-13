import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from "@angular/forms";

import {AppComponent} from './app.component';
import {HeaderComponent} from './header/header.component';
import {ContentComponent} from './content/content.component';
import {SearchPageComponent} from './content/search-page/search-page.component';
import {SearchFilterComponent} from './content/search-page/search-filter/search-filter.component';
import {SearchResultsComponent} from './content/search-page/search-results/search-results.component';
import {AngularMultiSelectModule} from "angular2-multiselect-dropdown/angular2-multiselect-dropdown";
import {MultiselectComponent} from './content/search-page/search-filter/multiselect/multiselect.component';
import {QueryService} from "./query.service";

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    ContentComponent,
    SearchPageComponent,
    SearchFilterComponent,
    SearchResultsComponent,
    MultiselectComponent
  ],
  imports: [
    BrowserModule,
    AngularMultiSelectModule,
    FormsModule
  ],
  providers: [QueryService],
  bootstrap: [AppComponent]
})
export class AppModule { }
