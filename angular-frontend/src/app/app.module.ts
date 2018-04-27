import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";

import {AppComponent} from './app.component';
import {HeaderComponent} from './header/header.component';
import {SearchPageComponent} from './header/content/search-page/search-page.component';
import {SearchFormComponent} from './header/content/search-page/search-form/search-form.component';
import {SearchResultsComponent} from './header/content/search-page/search-results/search-results.component';
import {AngularMultiSelectModule} from "angular2-multiselect-dropdown/angular2-multiselect-dropdown";
import {MultiselectComponent} from './header/content/search-page/search-form/multiselect/multiselect.component';
import {QueryService} from "./query.service";
import {ResultComponent} from './header/content/search-page/search-results/result/result.component';
import {PaginationComponent} from './header/content/search-page/search-results/pagination/pagination.component';
import {DetailService} from "./detail.service";
import {DetailsPageComponent} from './header/content/details-page/details-page.component';
import {CreditsComponent} from './header/content/details-page/credits/credits.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    SearchPageComponent,
    SearchFormComponent,
    SearchResultsComponent,
    MultiselectComponent,
    ResultComponent,
    PaginationComponent,
    DetailsPageComponent,
    CreditsComponent
  ],
  imports: [
    BrowserModule,
    AngularMultiSelectModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [QueryService, DetailService],
  bootstrap: [AppComponent]
})
export class AppModule { }
