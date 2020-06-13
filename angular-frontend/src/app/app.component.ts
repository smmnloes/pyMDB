import {Component, OnInit} from '@angular/core';
import {Event, NavigationEnd, NavigationStart, Router} from "@angular/router";
import {filter, observeOn, scan} from "rxjs/operators";
import {asyncScheduler} from "rxjs";

// modified version of
// https://medium.com/angular-in-depth/reactive-scroll-position-restoration-with-rxjs-792577f842c
interface ScrollPositionRestore {
  event: Event;
  positions: { [K: number]: number };
  trigger: 'imperative' | 'popstate' | 'hashchange';
  idToRestore: number;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'pyMDB - Movie search';


  constructor(private router: Router) {}

  ngOnInit() {
    this.router.events
      .pipe(
        filter(
          event =>
            event instanceof NavigationStart || event instanceof NavigationEnd,
        ),
        scan<Event, ScrollPositionRestore>((acc, event) => ({
          event,
          positions: {
            ...acc.positions,
            ...(event instanceof NavigationStart
              ? {
                [event.id]: document.documentElement.scrollTop,
              }
              : {}),
          },
          trigger:
            event instanceof NavigationStart
              ? event.navigationTrigger
              : acc.trigger,
          idToRestore:
            (event instanceof NavigationStart &&
              event.restoredState &&
              event.restoredState.navigationId + 1) ||
            acc.idToRestore,
        })),
        filter(
          ({ event, trigger }) => event instanceof NavigationEnd && !!trigger,
        ),
        observeOn(asyncScheduler),
      )
      .subscribe(({ trigger, positions, idToRestore }) => {
        if (trigger === 'imperative') {
          document.documentElement.scrollTop = 0;
        }
        if (trigger === 'popstate') {
          setTimeout(()=>document.documentElement.scrollTop = positions[idToRestore], 100);
        }
      });
  }

}

