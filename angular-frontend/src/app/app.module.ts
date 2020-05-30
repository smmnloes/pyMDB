import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";

import {AppComponent} from './app.component';
import {HeaderComponent} from './header/header.component';
import {SearchPageComponent} from './header/content/search-page/search-page.component';
import {SearchFormComponent} from './header/content/search-page/search-form/search-form.component';
import {SearchResultsComponent} from './header/content/search-page/search-results/search-results.component';
import {QueryService} from "./services/query.service";
import {ResultComponent} from './header/content/search-page/search-results/result/result.component';
import {PaginationComponent} from './header/content/search-page/search-results/pagination/pagination.component';
import {DetailService} from "./services/detail.service";
import {DetailsPageComponent} from './header/content/details-page/details-page.component';
import {CreditsComponent} from './header/content/details-page/credits/credits.component';
import {AppRoutingModule} from "./app-routing-module"
import {FooterComponent} from './header/footer/footer.component';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {ToastrModule} from "ngx-toastr";
import {MultiSelectAllModule} from "@syncfusion/ej2-angular-dropdowns";

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    SearchPageComponent,
    SearchFormComponent,
    SearchResultsComponent,
    ResultComponent,
    PaginationComponent,
    DetailsPageComponent,
    CreditsComponent,
    FooterComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    MultiSelectAllModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot({positionClass: 'toast-top-center', timeOut: 3000})
  ],
  providers: [QueryService, DetailService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
