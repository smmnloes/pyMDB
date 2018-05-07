import {Routes} from "@angular/router";
import {SearchPageComponent} from "./header/content/search-page/search-page.component";
import {DetailsPageComponent} from "./header/content/details-page/details-page.component";

export const appRoutes: Routes = [
  {path: '', redirectTo: "/search", pathMatch: 'full'},
  {path: 'search', component:SearchPageComponent},
  {path: 'details', component: DetailsPageComponent},
  {path: 'details/:movieId', component: DetailsPageComponent},
];
